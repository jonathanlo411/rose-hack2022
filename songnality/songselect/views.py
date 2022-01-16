# Django Imports
from re import search
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt

# Other Imports
import os, json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import collections


# API Helper Functions

# Authorization function
def authorize_user(client_id, client_secret, redirect_uri):
    scope = 'user-library-read playlist-read-private user-top-read'
    auth_link=SpotifyOAuth(client_id=client_id,client_secret=client_secret, redirect_uri=redirect_uri,scope=scope).get_authorize_url()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,client_secret=client_secret, redirect_uri=redirect_uri"""maybe put auth url here?""",scope=scope))



# Print out list of song objects with name, artist, and picture
def get_top_tracks(SP):
    top_tracks = []

    top_query = SP.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')['items']
    for entry in top_query:
        artists = []
        for artist in entry['artists']:
            artists.append(artist['name'])
        top_tracks.append({'artists': artists, 'track_id': entry['id'], 'name': entry['name'], 'preview_url': entry['preview_url'], 'image': entry['album']['images'][-1]['url']})
    
    for track in top_tracks:
        if len(track['artists']) > 1:
            track['display_info'] = track['name'] + ' by ' + ' and '.join(track['artists'])
        else:
            track['display_info'] = track['name'] + ' by ' + track['artists'][0]
    
    return top_tracks

# Create function to return list of search results based on search query
def search_tracks(query, SP):
    search_results = SP.search(q=query, type='track,artist')
    search_tracks = []

    for entry in search_results['tracks']['items']:
        artists = []
        for artist in entry['artists']:
            artists.append(artist['name'])
        search_tracks.append({'artists': artists, 'track_id': entry['id'], 'name': entry['name'], 'preview_url': entry['preview_url'], 'image': entry['album']['images'][-1]['url']})
    
    for track in search_tracks:
        if len(track['artists']) > 1:
            track['display_info'] = track['name'] + ' by ' + ' and '.join(track['artists'])
        else:
            track['display_info'] = track['name'] + ' by ' + track['artists'][0]
    
    return search_tracks

# Create list of current user's playlists
def query_playlists(SP):
    playlists_list = []
    playlists = SP.current_user_playlists(limit=50, offset=0)['items']
    for playlist in playlists:
        playlists_list.append({'name': playlist['name'], 'display_info': (playlist['name'] + ' by ' + playlist['owner']['display_name']), 'owner': playlist['owner']['display_name'], 'playlist_id': playlist['id'], 'image': playlist['images'][-1]['url']})
    return playlists_list

# Query a playlist's id by name from a list of playlists
def query_playlist_id(playlist_name, playlist_list):
    return next(item for item in playlist_list if item["name"] == playlist_name)['playlist_id']

# Create function that returns list of tracks in specified playlist
def tracks_in_playlist(username, playlist_id, SP):
    playlist_tracks = []

    playlist_query = SP.user_playlist_tracks(username, playlist_id)['items']
    for entry in playlist_query:
        artists = []
        for artist in entry['track']['artists']:
            artists.append(artist['name'])

        playlist_tracks.append({'artists': artists, 'track_id': entry['track']['id'], 'name': entry['track']['name'], 'preview_url': entry['track']['preview_url'], 'image': entry['track']['album']['images'][-1]['url']})
    return playlist_tracks

def get_track_features(track_ids, SP):
    audio_features = SP.audio_features(track_ids)
    return audio_features

def average_features(list_of_features):
    numeric_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']
    numeric_values = [{ your_key: dict_entry[your_key] for your_key in numeric_features } for dict_entry in list_of_features]
    
    counter = collections.Counter()
    for d in numeric_values: 
        counter.update(d)
        
    return {k: v / len(list_of_features) for k, v in dict(counter).items()}



# Render

@csrf_exempt
# Create your views here.
def songselect(request):
    # Obtaining info
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = open(os.path.join(script_dir, 'config.json'))
    config = json.load(config_file)
    config_file.close()

    # Intializing variables
    ID = config['ID']
    SECRET = config['SECRET']
    SP = authorize_user(ID, SECRET, 'http://127.0.0.1:8000/songselect')
    s = query_playlists(SP)
    
    # Initial Page Load
    context = {
        "sform": SearchForm,
        "s": s
    }
    return render(request, 'songselect/songselect.html', context)

@csrf_exempt
def searchsong(request):
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = open(os.path.join(script_dir, 'config.json'))
    config = json.load(config_file)
    config_file.close()

    # Intializing variables
    ID = config['ID']
    SECRET = config['SECRET']
    SP = authorize_user(ID, SECRET, 'https://www.google.com/')

    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form['search']
            results = search_tracks(search, SP)
            jsonResults = json.dumps(results)
            return JsonResponse(jsonResults, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    print('here')
    return JsonResponse({"error": ""}, status=400)


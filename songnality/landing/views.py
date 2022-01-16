from django.shortcuts import render
from songselect.views import authorize_user1

import os, json

# Create your views here.

def landing(request):
    # Obtaining info
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = open(os.path.join(script_dir, 'config.json'))
    config = json.load(config_file)
    config_file.close()

    # Intializing variables
    ID = config['ID']
    SECRET = config['SECRET']
    url = "http://127.0.0.1:8000/songselect"
    link = authorize_user1(ID, SECRET, url)
    context = {
        "alink": link
    }
    return render(request, 'landing/landing.html', context)

def about(request):
    return render(request, 'landing/about.html')

def pinfo(request):
    return render(request, 'landing/pinfo.html')
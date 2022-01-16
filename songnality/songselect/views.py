# Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt

# Other Imports
import os, json

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
    
    # Initial Page Load
    context = {
        "sform": SearchForm
    }
    return render(request, 'songselect/songselect.html', context)

@csrf_exempt
def searchsong(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        form = SearchForm(request.POST)
        print(form)
        if form.is_valid():
            search = form['search']
            # serialize in new friend object in json
            # send to client side.
            return JsonResponse({"instance": search}, status=200)
        else:
            # some form errors occured.
            print("ahh")
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    print('here')
    return JsonResponse({"error": ""}, status=400)



# API Helper Functions
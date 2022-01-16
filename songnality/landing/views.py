from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(request, 'landing/landing.html')

def about(request):
    return render(request, 'landing/about.html')

def pinfo(request):
    return render(request, 'landing/pinfo.html')
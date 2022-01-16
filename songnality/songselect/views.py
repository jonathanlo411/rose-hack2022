from django.shortcuts import render

# Create your views here.
def songselect(request):
    return render(request, 'songselect/songselect.html')
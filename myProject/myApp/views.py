from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'myApp/home.html')

def about(request):
    return render(request, 'myApp/about.html')

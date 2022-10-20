from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def home3(request):
    return render(request,'index2.html')

def events(request):
    return render(request,'Events.html')
from django.shortcuts import render

from main.models import *

# Create your views here.
def home(request):
    return render(request,'home.html')

def home3(request):
    return render(request,'index2.html')

def events(request):
    return render(request,'Events.html')

def showcat(request):
    cat = EventCategory.objects.all()
    staff = UserProfile.objects.filter(is_staff=True)
    event = Event.objects.all()
    context={'cat': cat, 'staffs': staff,'events': event}
    return render(request,'showcategory.html', context)
import os
from django.shortcuts import render,redirect

from main.models import *
from django.db.models import Count

# Create your views here.
def home(request):
    return render(request,'home.html')

def home3(request):
    return render(request,'index2.html')

def events(request):
    return render(request,'events/Events.html')

def showcat(request):
    cate = EventCategory.objects.all()
    staff = UserProfile.objects.filter(is_staff=True)
    context={'cat': cate, 'staffs': staff}
    return render(request,'events/showcategory.html', context)

def add_category(request):
    if request.method=='POST':
        cat=EventCategory()
        cat.name = request.POST['name']
        cat.code = request.POST['code']
        sel1 = request.POST['sel']
        usr = UserProfile.objects.get(id=sel1)
        cat.head = usr
        cat.image = request.FILES['image']
        cat.save()
        return redirect('showcat')
    return redirect('showcat')

def deleteCategory(request,pk):
    pp = EventCategory.objects.get(id=pk)
    if pp.image is not None:
        if not pp.image == "/static/image/default.png":
            os.remove(pp.image.path)
        else:pass
    pp.delete()
    return redirect('showcat')

def showmanagers(request):
    cate = EventCategory.objects.all()
    staff = UserProfile.objects.filter(is_staff=True)
    context={'cat': cate, 'staffs': staff}
    return render(request,'events/showmanagers.html', context)
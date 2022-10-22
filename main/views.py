import os
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from main.models import *
from django.db.models import Count
from django.conf import settings
from django.utils import timezone

# Create your views here.
def home(request):
    today=timezone.now()
    evening=Event.objects.filter(scheduled_status=True)
    eveningup=evening.filter(status='Upcoming')

    eve=evening.filter(status='Ongoing').count()
    evethisyear=evening.filter(status='Completed',end_date__year=today.year).count()
    eveallyear=evening.filter(status='Completed').count()

    evenup7=eveningup.filter(start_date__lte=(today+timezone.timedelta(days = 7))).count()
    evenupcoming=eveningup.filter(start_date__lte=(today+timezone.timedelta(days = 57))).count()-evenup7
    eveupyear=eveningup.filter(start_date__lte=(today+timezone.timedelta(days = 187))).count()-evenupcoming-evenup7
    
    mngrs=UserProfile.objects.filter(is_staff=True).count()
    usr=UserProfile.objects.filter(is_staff=False)
    usrs=usr.count()
    nwusrday=usr.filter(start_date=today).count()

    evests=Event.objects.filter(scheduled_status=False).count()
    
    context={'Ongoing':eve,'Completed':evethisyear,'Completedall':eveallyear,'managers':mngrs,'users':usrs,'schedule':evests,
            'newUserToday':nwusrday,'Upcomingyears':eveupyear,'Upcoming':evenupcoming,'seven':evenup7}
    return render(request,'home.html',context)

def home3(request):
    return render(request,'index2.html')

def events(request):
    return render(request,'events/Events.html')

def showcat(request):
    cate = EventCategory.objects.all()
    staff = UserProfile.objects.filter(is_staff=True, is_active=True)
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
    events = Event.objects.filter(status='Ongoing')
    eventsup = Event.objects.filter(status='Upcoming')
    context={'cat': cate, 'staffs': staff,'events': events,'eventsup': eventsup}
    return render(request,'events/showmanagers.html', context)


def addManager(request):
    if request.method=='POST':
        cat=UserProfile()
        cat.user_name = request.POST['uname']
        cat.first_name = request.POST['fname']
        cat.last_name = request.POST['lname']
        cat.email = request.POST['email']
        cat.mobile = request.POST['mob']
        cat.alt_mobile = request.POST['amob']
        cat.gender = request.POST['gender']
        cat.is_staff=True
        cat.image = request.FILES['image']
        password = UserProfile.objects.make_random_password()
        cat.set_password(password)
        if not UserProfile.objects.filter(user_name=cat.user_name).exists():
            if not UserProfile.objects.filter(email=cat.email).exists():
                cat.save()
                message = '\nYour Temporary password is \n\n'+password+'\n\nReset on login '
                print(message)
                send_mail(
                'Welcome to My Catering project',
                message,
                settings.EMAIL_HOST_USER,
                [cat.email],
                fail_silently=False,
                )
                return redirect('showmanagers')
            else:
                print('email')
        else:
            print('username')
    return redirect('showmanagers')

def deleteManager(request,pk):
    pp = UserProfile.objects.get(id=pk)
    if pp.image is not None:
        if not pp.image == "/static/image/default.png":
            os.remove(pp.image.path)
        else:pass
    pp.delete()
    return redirect('showmanagers')
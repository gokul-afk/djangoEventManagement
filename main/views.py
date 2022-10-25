import os
from sre_parse import CATEGORIES
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

def catlist(request,pk):
    if not FoodCategory.objects.get(name=pk).is_leaf_node():
        categories=FoodCategory.objects.get(name=pk).get_children().order_by('order')
        context = {'cat':categories,'branch':pk,'product':False}
    else:
        categor= FoodCategory.objects.get(name=pk)
        categories=FoodProducts.objects.filter(category=categor)
        context = {'cat':categories,'branch':pk,'product':True}
    return render(request,'catering/listcat.html',context)

def product(request,pk):
    pt=FoodProducts.objects.get(name=pk)
    price4=(pt.price*4)
    price8=(pt.price*8)-((pt.price//10)*4)
    pr=pt.pair
    
    pcat=FoodProducts.objects.filter(category__in=FoodCategory.objects.get(name=pt.paircategory.name).get_descendants(include_self=False))
    if not pt.pair == None:
        pcat=FoodProducts.objects.filter(category__in=FoodCategory.objects.get(name=pt.paircategory.name).get_descendants(include_self=False)).exclude(name=pr.name)
    if pt.paircategory.is_leaf_node():
        pcat=FoodProducts.objects.filter(category=pt.paircategory)
        if not pt.pair == None:
            pcat=FoodProducts.objects.filter(category=pt.paircategory).exclude(name=pr.name)

    context = {'pdt':pt,'eight':price8,'four':price4,'pair':pr,'paircat':pcat}
    return render(request,'catering/product.html',context)


def addtocart(request,pk):
    if request.method=='POST':
        pt=FoodProducts.objects.get(name=pk)
        portion = int(request.POST['sel'])
        quant= int(request.POST['count'])
        if not quant == 0:    
            addcart(request,pt.id,quant,portion)
            if not pt.pair == None:
                pairnum = request.POST['selpair']
                if not pairnum == 'no':
                    addcart(request,pt.pair.id,quant,int(pairnum))
            if not pt.paircategory.id == 19:
                catnip = request.POST['selcate']
                if not catnip == 'no':
                    addcart(request,catnip,quant,4)
    return redirect((request.META.get('HTTP_REFERER')))


def addcart(request,pk,quant,portion):
    pt=FoodProducts.objects.get(id=pk)
    usr= UserProfile.objects.get(user_name=request.user)
    pric=0
    print(portion)
    print(type(portion))
    if portion==4:
        quant*=4
        pric=pt.price*quant
        print(pric)
    elif portion==8:
        quant*=8
        pric=(pt.price*8)-((pt.price//10)*4)
        print(pric)
    if FoodCart.objects.filter(customer_id=usr.id, product_id=pk).exists():
        o=FoodCart.objects.get(customer_id=usr.id, product_id=pk)
        o.quantity+=quant
        o.price+=pric
        o.save()
    else:
        o=FoodCart()
        o.product=pt
        o.customer=usr
        o.quantity=quant
        o.price=pric
        o.save()

def showcart(request,pk):
    usr= UserProfile.objects.get(id=pk)
    c=FoodCart.objects.filter(customer_id=usr.id)
    sum=0
    for i in c:
        sum+=i.price
    context={'carts':c,'sum':sum,}
    return render(request,'catering/cart.html',context)

def events(request,sort,st):
    if st=='Up':
        Events = Event.objects.all().order_by(sort)
    else:
        Events = Event.objects.filter(status=st).order_by(sort)
    cat=EventCategory.objects.all()
    staff= UserProfile.objects.filter(is_staff=True,is_active=True).exclude(is_superuser=True)
    context = {'events':Events,'st':st,'Categories':cat,'staffs':staff}
    return render(request,'events/Events.html',context)

def eventshow(request,pk):
    Events = Event.objects.get(id=pk)
    images = EventImage.objects.filter(event=Events)
    all = EventImage.objects.filter(event = Events, type="all")
    context = {'event':Events,'images':images,'all':all}
    return render(request,'events/EventsDetails.html',context)    

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
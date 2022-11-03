import os
from sre_parse import CATEGORIES
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from main.models import *
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import auth
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required

# Create your views here.
def dashboard(request):
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
    ordrs = FoodOrder.objects.filter(status="Processing").count()
    orderuser=FoodOrder.objects.values('customer_id').distinct().count()

    myorder=FoodOrder.objects.filter(customer=request.user)
    Processing = myorder.filter(status="Processing").count()
    Cancelled = myorder.filter(status="Cancelled").count()

    context={'Ongoing':eve,'Completed':evethisyear,'Completedall':eveallyear,'managers':mngrs,'users':usrs,'schedule':evests,
            'newUserToday':nwusrday,'Upcomingyears':eveupyear,'Upcoming':evenupcoming,'seven':evenup7,'orders':ordrs,'orderuser':orderuser,
            'Processing':Processing,'Cancelled':Cancelled,}
    return render(request,'dashboard.html',context)

def home(request):
    print(request.user)
    return render(request,'home.html')

def profile(request,pk):
    user = UserProfile.objects.get(id=pk)
    myorder=FoodOrder.objects.filter(customer=user)
    Events = Event.objects.filter(customer=user)
    Processing = myorder.filter(status="Processing").count()
    Processing = myorder.filter(status="Processing").count()
    Cancelled = myorder.filter(status="Cancelled").count()
    Approved = myorder.filter(status="Approved").count()
    context = {'user':user,'Processing':Processing,'Cancelled':Cancelled,'Approved':Approved,'Events':Events,}
    return render(request,'profile.html',context)


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
    Events = Event.objects.filter(customer=request.user)
    context = {'pdt':pt,'eight':price8,'four':price4,'pair':pr,'paircat':pcat,'Event':Events,}
    return render(request,'catering/product.html',context)


def addtocart(request,pk):
    if request.method=='POST':
        if request.POST['event'] == 'none':
            return redirect('eventadd')
        eve=int(request.POST['event'])
        pt=FoodProducts.objects.get(name=pk)
        portion = int(request.POST['sel'])
        quant= int(request.POST['count'])
        if not quant == 0:    
            addcart(request,pt.id,quant,portion,eve)
            if not pt.pair == None:
                pairnum = request.POST['selpair']
                if not pairnum == 'no':
                    addcart(request,pt.pair.id,quant,int(pairnum),eve)
            if not pt.paircategory.id == 19:
                catnip = request.POST['selcate']
                if not catnip == 'no':
                    addcart(request,catnip,quant,4,eve)
    return redirect('showcart',pk=request.user.id)


def addcart(request,pk,quant,portion,eve):
    pt=FoodProducts.objects.get(id=pk)
    event = Event.objects.get(id=eve)
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
    if menuCart.objects.filter(customer_id=usr.id, product_id=pk,event_id=event.id).exists():
        o=menuCart.objects.get(customer_id=usr.id, product_id=pk,event_id=event.id)
        o.quantity+=quant
        o.price+=pric
        o.save()
        
    else:
        o=menuCart()
        o.product=pt
        o.customer=usr
        o.quantity=quant
        o.price=pric
        o.event=event
        o.save()

def order(request,pk):
    usr= UserProfile.objects.get(id=pk)
    c=menuCart.objects.filter(customer_id=usr.id)
    for i in c:
        o = FoodOrder()
        o.product = i.product
        o.customer = i.customer
        o.quantity = i.quantity
        o.price = i.price
        o.save()
        i.delete()
    return redirect((request.META.get('HTTP_REFERER')))

def showorder(request, pk):
    usr= UserProfile.objects.get(id=pk)
    c=FoodOrder.objects.filter(customer_id=usr.id)
    sum=0
    for i in c:
        sum+=i.price
    context={'carts':c,'sum':sum,}
    return render(request,'catering/order.html',context)



def showcart(request,pk):
    usr= UserProfile.objects.get(id=pk)
    c=menuCart.objects.filter(customer_id=usr.id)
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
    staff= UserProfile.objects.filter(is_staff=True,is_active=True,is_pass=True)
    context = {'events':Events,'st':st,'Categories':cat,'staffs':staff}
    return render(request,'events/Events.html',context)

def eventshow(request,pk):
    Events = Event.objects.get(id=pk)
    eventlat=Events.location[0]
    eventlong=Events.location[1]
    print(eventlat)
    images = EventImage.objects.filter(event=Events)
    all = EventImage.objects.filter(event = Events, type="all")
    context = {'event':Events,'images':images,'all':all,'locationlat':eventlat,'locationlong':eventlong}
    return render(request,'events/EventsDetails.html',context)    

def eventadd(request):
    Cat = EventCategory.objects.all()
    context = {'categories':Cat,}
    return render(request,'events/eventadd.html',context) 


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

def showusers(request):
    users = UserProfile.objects.filter(is_staff=False,is_active=True)
    context={ 'staffs': users,}
    return render(request,'showusers.html', context)

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
        if request.FILES.get('image') is not None:
            cat.image = request.FILES['image']
        else:
            cat.image = "/static/image/default.png"
        password = UserProfile.objects.make_random_password()
        print(password)
        cat.set_password(password)
        if not UserProfile.objects.filter(user_name=cat.user_name).exists():
            if not UserProfile.objects.filter(email=cat.email).exists():
                cat.save()
                message = '\nYour Temporary password is \n\n'+password+'\n\nReset on login \n\n\nGo to Profile (end of page)'
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

def addevent(request):
    if request.method=='POST':
        cat=Event()
        cat.name = request.POST['name']
        cat.description = request.POST['desc']
        cater = request.POST['sel']
        cat.category = EventCategory.objects.get(id=cater)
        maner = request.POST['man']
        if maner == 'same':
            maner = cat.category.head.user_name
        cat.manager = UserProfile.objects.get(user_name=maner)
        cat.start_date = request.POST['sdate']
        cat.end_date = request.POST['edate']
        cat.venue = request.POST['venue']
        cat.maximum_attende = request.POST['maxattend']
        cat.save()
        return redirect((request.META.get('HTTP_REFERER')))
    return redirect('home')

def editevent(request,pk):
    if request.method=='POST':
        cat=Event.objects.get(id=pk)
        cat.name = request.POST['name']
        cater = request.POST['sel']
        cat.category = EventCategory.objects.get(id=cater)
        maner = request.POST['man']
        if maner == 'same':
            maner = cat.category.head.id
        cat.scheduled_status= int(request.POST['scheduled'])
        cat.status= request.POST['status']
        cat.manager = UserProfile.objects.get(id=maner)
        cat.start_date = request.POST['sdate']
        cat.end_date = request.POST['edate']
        cat.venue = request.POST['venue']
        cat.maximum_attende = request.POST['maxattend']
        cat.save()
        return redirect((request.META.get('HTTP_REFERER')))


def addeventuser(request):
    if request.method ==  'POST':
        cat=Event()
        cat.name = request.POST['name']
        cat.description = request.POST['desc']
        cater = request.POST['sel']
        cat.category = EventCategory.objects.get(id=cater)
        cat.customer = UserProfile.objects.get(user_name=request.user)
        cat.start_date = request.POST['sdate']
        cat.end_date = request.POST['edate']
        cat.venue = request.POST['venue']
        cat.contact = request.POST['contact']
        cat.maximum_attende = request.POST['maxattend']
        cat.status = 'Requested'
        cat.save()
        eve = Event.objects.get(name=cat.name)
        return redirect('menus',pk=eve.id) 
    return redirect('home')

def menus(request,pk):
    if not pk==0:
        Events = Event.objects.get(id=pk)
    else:
        Events = Event.objects.filter(customer=request.user)
    food = FoodProducts.objects.all()
    context = {'food':food,'Event':Events,'Eventall':pk}
    return render(request,'catering/menus.html',context)


def menucart(request,pk):
    if request.method=='POST':
        if not request.POST['event']=='none':
            eve=int(request.POST['event'])
        else:
            return redirect(eventadd)
        drink1=int(request.POST['drink1'])
        addmenucart(request,drink1,eve)
        drink2=int(request.POST['drink2'])
        addmenucart(request,drink2,eve)
        bread1=int(request.POST['bread1'])
        addmenucart(request,bread1,eve)
        chicken1=int(request.POST['chicken1'])
        addmenucart(request,chicken1,eve)
        rice1=int(request.POST['rice1'])
        addmenucart(request,rice1,eve)
        beef1=int(request.POST['beef1'])
        addmenucart(request,beef1,eve)
        fish1=int(request.POST['fish1'])
        addmenucart(request,fish1,eve)
        veg1=int(request.POST['veg1'])
        addmenucart(request,veg1,eve)
        veg2=int(request.POST['veg2'])
        addmenucart(request,veg2,eve)
        salad1=int(request.POST['salad1'])
        addmenucart(request,salad1,eve)
        salad2=int(request.POST['salad2'])
        addmenucart(request,salad2,eve)
        salad3=int(request.POST['salad3'])
        addmenucart(request,salad3,eve)
        dessert1=int(request.POST['dessert1'])
        addmenucart(request,dessert1,eve)
        return redirect('catlist',pk='All')
    return redirect((request.META.get('HTTP_REFERER')))


def addmenucart(request,pk,eve):
    product = FoodProducts.objects.get(id=pk)
    customer = UserProfile.objects.get(id=request.user.id)
    event = Event.objects.get(id=eve)
    if menuCart.objects.filter(customer_id=customer.id,product_id=product.id,event_id=event.id).exists():
        cart=menuCart.objects.get(customer_id=customer.id,product_id=product.id,event_id=event.id)
        cart.quantity+=cart.event.maximum_attende
        cart.price+=cart.event.maximum_attende * cart.product.price
        cart.save()
    else:
        cart = menuCart()
        cart.product=product
        cart.event=event
        cart.customer=customer
        cart.quantity = cart.event.maximum_attende
        cart.price = cart.quantity * cart.product.price
        cart.save()
    

def deleteevent(request,pk):
    pp = Event.objects.get(id=pk)
    pp.delete()
    return redirect((request.META.get('HTTP_REFERER')))


def deleteManager(request,pk):
    pp = UserProfile.objects.get(id=pk)
    if pp.image is not None:
        if not pp.image == "/static/image/default.png":
            os.remove(pp.image.path)
        else:pass
    pp.delete()
    return redirect('showmanagers')

def deletecart(request,pk):
    pp = menuCart.objects.get(id=pk)
    pp.delete()
    return redirect((request.META.get('HTTP_REFERER')))

def login(request):
    try:
        if request.method == 'POST':
            
            try:
                username = request.POST['username']
                password = request.POST['password']
                if not UserProfile.objects.filter(user_name=username):
                    user =UserProfile.objects.get(email=username)
                else:
                    user =UserProfile.objects.get(user_name=username)
                print(user)
                try:
                    validate_password(password, user)
                    print(password+"val succ"+user.password)
                    request.session["uid"] = user.id
                    print(request.session["uid"])
                    auth.login(request, user)
                    print(request.user.id)
                    return redirect((request.META.get('HTTP_REFERER')))
                except :
                    print("Validation error")
                    return render(request,'home')
            except:
                print( 'main code')
                return redirect((request.META.get('HTTP_REFERER')))
        else:
            return redirect((request.META.get('HTTP_REFERER')))
    except:
        print('whole code')
        return redirect((request.META.get('HTTP_REFERER')))

def reset(request):
    if request.method=='POST':
        user = UserProfile.objects.get(id=request.user.id)
        opassword=request.POST['opassword']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        try:
            validate_password(opassword, user)
            if password==cpassword:
                user.set_password(password)
                user.is_pass=True         
                user.save()
                print("success")
                return redirect('logout')
        except:
            print("validation failed")
            return redirect((request.META.get('HTTP_REFERER')))
    return redirect((request.META.get('HTTP_REFERER')))

def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('home')

def addUser(request):
    if request.method=='POST':
        cat=UserProfile()
        cat.user_name = request.POST['uname']
        cat.first_name = request.POST['fname']
        cat.last_name = request.POST['lname']
        
        cat.email = request.POST['email']
        cat.mobile = request.POST['mob']
        cat.alt_mobile = request.POST['amob']
        cat.gender = request.POST['gender']
        cat.image = "/static/image/default.png"
        password = UserProfile.objects.make_random_password()
        cat.set_password(password)
        if not UserProfile.objects.filter(user_name=cat.user_name).exists():
            if not UserProfile.objects.filter(email=cat.email).exists():
                cat.save()
                message = '\nYour Temporary password is \n\n'+password+'\n\nReset on login \n\n\nGo to Profile (end of page)'
                print(message)
                send_mail(
                'Welcome to My Catering project',
                message,
                settings.EMAIL_HOST_USER,
                [cat.email],
                fail_silently=False,
                )
                return redirect((request.META.get('HTTP_REFERER')))
            else:
                print('email')
        else:
            print('username')
    return redirect((request.META.get('HTTP_REFERER')))
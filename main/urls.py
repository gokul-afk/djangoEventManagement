from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('profile/<int:pk>/',views.profile,name='profile'),
    path('wedding/',views.wedding,name='wedding'),
    path('parties/',views.parties,name='parties'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('catlist/<str:pk>/',views.catlist,name='catlist'),
    path('adduser/',views.addUser,name='adduser'),


    path('events/<str:sort>/<str:st>/',views.events,name='events'),
    path('eventshow/<int:pk>/',views.eventshow,name='eventshow'),
    path('addevent/',views.addevent,name='addevent'),
    path('addeventuser/',views.addeventuser,name='addeventuser'),
    path('eventadd/',views.eventadd,name='eventadd'),
    path('editevent/<int:pk>/',views.editevent,name='editevent'),
    path('deleteevent/<int:pk>',views.deleteevent,name='deleteevent'),
    path('showusers/',views.showusers,name='showusers'),

    path('menus/<int:pk>/',views.menus,name='menus'),
    path('menucart/<str:pk>/',views.menucart,name='menucart'),
    path('product/<str:pk>/',views.product,name='product'),
    path('addtocart/<str:pk>/',views.addtocart,name='addtocart'),
    path('showcart/<int:pk>/',views.showcart,name='showcart'),
    path('deletecart/<int:pk>',views.deletecart,name='deletecart'),
    path('order/<int:pk>',views.order,name='order'),
    path('showorder/<int:pk>/',views.showorder,name='showorder'),

    path('showcat/',views.showcat,name='showcat'),
    path('add_category/',views.add_category,name='add_category'),
    path('deleteCategory/<int:pk>',views.deleteCategory,name='deleteCategory'),

    path('showmanagers/',views.showmanagers,name='showmanagers'),
    path('addManager/',views.addManager,name='addManager'),
    path('deleteManager/<int:pk>',views.deleteManager,name='deleteManager'),
    
    path('logout/',views.logout,name="logout"),
    path('login/',views.login,name="login"),
    path('reset/',views.reset,name="reset"),

]

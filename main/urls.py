from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('catlist/<str:pk>/',views.catlist,name='catlist'),
    path('events/<str:sort>/<str:st>/',views.events,name='events'),
    path('eventshow/<int:pk>/',views.eventshow,name='eventshow'),
    path('product/<str:pk>/',views.product,name='product'),
    path('addtocart/<str:pk>/',views.addtocart,name='addtocart'),
    path('showcart/<int:pk>/',views.showcart,name='showcart'),

    path('showcat/',views.showcat,name='showcat'),
    path('add_category/',views.add_category,name='add_category'),
    path('deleteCategory/<int:pk>',views.deleteCategory,name='deleteCategory'),

    path('showmanagers/',views.showmanagers,name='showmanagers'),
    path('addManager/',views.addManager,name='addManager'),
    path('deleteManager/<int:pk>',views.deleteManager,name='deleteManager'),

]

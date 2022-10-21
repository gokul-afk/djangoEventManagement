from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('home3/',views.home3,name='home3'),
    path('events/',views.events,name='events'),

    path('showcat/',views.showcat,name='showcat'),
    path('add_category/',views.add_category,name='add_category'),
    path('deleteCategory/<int:pk>',views.deleteCategory,name='deleteCategory'),

    path('showmanagers/',views.showmanagers,name='showmanagers'),
    path('addManager/',views.addManager,name='addManager'),
    path('deleteManager/<int:pk>',views.deleteManager,name='deleteManager'),

]

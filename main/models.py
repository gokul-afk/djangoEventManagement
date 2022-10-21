from asyncio.windows_events import NULL
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from ckeditor.fields import RichTextField
from mapbox_location_field.models import LocationField  

# Create your models here.
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        if not user_name:
            raise ValueError(_('You must provide a user name'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                            first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to a staff')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to a superuser=True')

        return self.create_user(email, user_name, first_name, password, **other_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateField(default=timezone.now)
    mobile= models.CharField(max_length=255)
    alt_mobile= models.CharField(max_length=255,default=None,null=True,blank=True)
    gender = models.CharField(max_length=150)
    image = models.ImageField(upload_to='managers/')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','mobile']

    def __str__(self):
        return self.user_name

class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=7, unique=True)
    image = models.ImageField(upload_to='event_category/')
    head = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='category_user')
    def __str__(self):
        return self.name
    

class Event(models.Model):
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='event_category')
    name = models.CharField(max_length=255, unique=True)
    description = RichTextField()
    scheduled_status = models.BooleanField(default=False)
    venue = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = LocationField()
    maximum_attende = models.PositiveIntegerField()
    manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='event_user')
    created_date = models.DateField(editable=False,default=timezone.now)
    updated_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        if not self.id:
            self.created_date = timezone.now()
        self.updated_date = timezone.now()
        return super(Event, self).save(*args, **kwargs)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')
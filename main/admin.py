from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import UserProfile,EventCategory,Event,EventImage,FoodCategory,FoodProducts
from django.contrib.auth.admin import UserAdmin
from mapbox_location_field.admin import MapAdmin

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name','first_name',)
    list_filter = ('email','user_name','first_name','is_active','is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name',
        'first_name','is_superuser', 'is_active',
        'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name','mobile')}),
        ('NotRequired', {'fields': ('last_name', 'alt_mobile', 'gender','image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name','gender','last_name','mobile', 'alt_mobile','image','password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 10

# Register your models here.
admin.site.register(UserProfile, UserAdminConfig)

admin.site.register(EventCategory)

admin.site.register(Event, MapAdmin)

admin.site.register(EventImage)

admin.site.register(FoodCategory,CustomMPTTModelAdmin)

admin.site.register(FoodProducts)

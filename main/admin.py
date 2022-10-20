from django.contrib import admin
from .models import UserProfile,EventCategory
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name','first_name',)
    list_filter = ('email','user_name','first_name','is_active','is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name',
        'first_name', 'last_name', 'is_active',
        'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name','last_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

# Register your models here.
admin.site.register(UserProfile, UserAdminConfig)

admin.site.register(EventCategory)
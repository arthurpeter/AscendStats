# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Climb

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': (
            'date_of_birth', 
            'sex', 
            'country', 
            'height', 
            'weight',
            'ape_index',
            'max_grade',
            'current_flash_grade'
        )}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Climb)
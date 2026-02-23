from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Wasifu wa Mwanachama', {'fields': (
            'full_name', 'phone', 'registration_number', 
            'date_of_birth', 'mkoa_wa_makazi', 'kanisa_analosali', 
            'course', 'year_of_study', 'gender', 'group', 'profile_image'
        )}),
    )
    list_display = ['username', 'full_name', 'registration_number', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)

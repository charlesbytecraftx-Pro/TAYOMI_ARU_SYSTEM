from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Taarifa za Utambulisho
    full_name = models.CharField(max_length=255, null=True, blank=True)
    # Muhimu: Tumeondoa unique=True kwa muda ili kuruhusu migration ipite bila Error ya SQLite
    phone = models.CharField(max_length=15, null=True, blank=True) 
    registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Taarifa za Binafsi na Mahali
    date_of_birth = models.DateField(null=True, blank=True)
    mkoa_wa_makazi = models.CharField(max_length=100, null=True, blank=True)
    kanisa_analosali = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    
    # Elimu na Kundi
    course = models.CharField(max_length=100, null=True, blank=True)
    year_of_study = models.CharField(max_length=20, null=True, blank=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True)
    
    role = models.CharField(max_length=20, default='Member')

    # Picha ya Wasifu
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.png')

    # Inaongeza phone kwenye mahitaji ya lazima (mfano wakati wa createsuperuser)
    REQUIRED_FIELDS = ['phone', 'email']

    def __str__(self):
        return self.full_name if self.full_name else self.username

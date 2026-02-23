from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Tumeongeza phone hapa kando ya email na username
        fields = ['username', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control shadow-sm',
                'placeholder': f'Enter {self.fields[field].label}'
            })

class ProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('', '-- Select Gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'phone', 'registration_number', 'date_of_birth', 
            'mkoa_wa_makazi', 'kanisa_analosali', 'course', 
            'year_of_study', 'gender', 'group', 'profile_image'
        ]
        labels = {
            'full_name': 'Full Name',
            'phone': 'Phone Number',
            'registration_number': 'Registration Number',
            'date_of_birth': 'Date of Birth',
            'mkoa_wa_makazi': 'Region of Residence',
            'kanisa_analosali': 'Church/Branch',
            'course': 'Course of Study',
            'year_of_study': 'Year of Study',
            'group': 'Assigned Group',
            'profile_image': 'Profile Picture'
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control shadow-sm'}),
            'group': forms.Select(attrs={'class': 'form-select shadow-sm'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control d-none', 'id': 'imageUpload', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'full_name' in self.fields:
            self.fields['full_name'].widget.attrs.update({'placeholder': 'Example: James Andrea Charles'})
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs.update({'placeholder': 'Example: 07XXXXXXXX'})
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control shadow-sm'})
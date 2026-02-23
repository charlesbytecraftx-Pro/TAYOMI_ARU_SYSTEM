from django import forms
from django.contrib.auth.models import User
from .models import Payment, Profile

class PaymentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'reference_number', 'receipt_image']
        labels = {
            'amount': 'Kiasi Ulichotuma',
            'reference_number': 'Namba ya Muamala (Reference No.)',
            'receipt_image': 'Picha ya Risiti/Screenshot',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mfano: 5000'}),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Mfano: RIC0W12345',
                'oninput': 'this.value = this.value.toUpperCase()'
            }),
            'receipt_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_reference_number(self):
        ref = self.cleaned_data.get('reference_number').strip().upper()
        # Inakagua kama namba hii imeshatumika na mtu mwingine yeyote
        if Payment.objects.filter(reference_number=ref).exists():
            raise forms.ValidationError(f"Namba ya muamala '{ref}' tayari imeshatumika. Kagua risiti yako.")
        return ref

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['first_name', 'last_name', 'email']}

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'profile_pic', 'department']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

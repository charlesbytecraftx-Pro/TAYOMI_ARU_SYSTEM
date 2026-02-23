from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Tumeongeza 'image' kwenye orodha ya fields
        fields = ['group', 'title', 'image', 'description', 'date', 'time', 'location']
        
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select rounded-pill shadow-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm', 'placeholder': 'Mfano: Morning Glory'}),
            'image': forms.FileInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-4 shadow-sm', 'rows': 3, 'placeholder': 'Maelezo mafupi...'}),
            'date': forms.DateInput(attrs={'class': 'form-control rounded-pill shadow-sm', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control rounded-pill shadow-sm', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm', 'placeholder': 'Wapi?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Logic yako ya zamani imebaki vile vile:
        self.fields['group'].required = False  # Inaruhusu tukio la jumla (null group)
        self.fields['group'].empty_label = "Tukio la Wanachama Wote (Jumla)"
        
        # Optional: Unaweza kuongeza label nzuri kwa ajili ya picha
        self.fields['image'].label = "Bango/Picha ya Tukio (Hiari)"

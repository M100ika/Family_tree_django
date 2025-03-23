from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 
                 'place_of_birth', 'biography', 'photo', 'parents']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 4}),
        } 
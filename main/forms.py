from django import forms
from .models import User
from django_countries.widgets import CountrySelectWidget

class ClimbForm(forms.Form):
    grade = forms.IntegerField(label="Grade", min_value=0, max_value=17, required=True)
    success = forms.BooleanField(label="Finished", required=False)
    attempts = forms.IntegerField(label="Number of Attempts", min_value=1, required=True)
    STYLE_CHOICES = [
        ('', 'Select'),
        ('Balance', 'Balance'),
        ('Dynamic', 'Dynamic'),
        ('Powerful', 'Powerful'),
        ('Technical', 'Technical'),
    ]
    style = forms.ChoiceField(label="Style", choices=STYLE_CHOICES, required=False)
    notes = forms.CharField(label="Notes", widget=forms.Textarea, required=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'date_of_birth', 
            'sex', 
            'country', 
            'height', 
            'weight', 
            'ape_index'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(choices=[
                ('', 'Select'), 
                ('M', 'Male'), 
                ('F', 'Female'), 
                ('O', 'Other')
            ]),
            'country': CountrySelectWidget(),
            'height': forms.NumberInput(attrs={'placeholder': 'cm'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'kg'}),
            'ape_index': forms.NumberInput(attrs={'placeholder': 'cm'}),
        }
        labels = {
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
            'ape_index': 'Ape Index (cm)',
            'date_of_birth': 'Date of Birth',
            'sex': 'Gender',
            'country': 'Nationality'
        }
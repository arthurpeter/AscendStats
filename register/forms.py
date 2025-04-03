from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from main.models import User
from django_countries.fields import CountryField


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Userame", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    country = CountryField(blank_label='Select Country').formfield(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    SEX_CHOICES = [
        ('', 'Select'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    sex = forms.ChoiceField(label="Sex", choices=SEX_CHOICES, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'country', 'date_of_birth', 'sex']

    def clean_email(self):
        """Ensure email is unique since it's the login field."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
    def save(self, commit=True):
        """Override save to set a hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=254, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

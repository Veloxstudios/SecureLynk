from django import forms
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'autocomplete': 'off',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'How can we help you?',
                'rows': 5,
            }),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
        }
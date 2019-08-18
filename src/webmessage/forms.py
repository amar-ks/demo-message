from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from webmessage.models import EmailBox


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required='Required. Inform  a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EmailForm(forms.ModelForm):

    class Meta:
        model = EmailBox
        fields = ['sender_name', 'subject', 'description']
        labels = {
            "sender_name": "To"
        }

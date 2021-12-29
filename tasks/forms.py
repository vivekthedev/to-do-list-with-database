from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class UserRegistration(forms.ModelForm):

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'name': 'title', 'placeholder': 'your password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'name': 'title', 'placeholder': 'confirm your password'}),
        strip=False,)

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True, 'name': 'title', 'placeholder': 'your username'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError('Your passwords did not match.')
        elif len(password2) < 8:
            raise forms.ValidationError(
                'Password can\'t be less than 8 characters.')
        return password2


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'name': 'title', 'placeholder': 'your username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'your password', 'name': 'title'
        }))

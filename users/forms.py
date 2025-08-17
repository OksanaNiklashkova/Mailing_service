from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """форма регистрации нового пользователя"""
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomAuthenticationForm(AuthenticationForm):
    pass

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

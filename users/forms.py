from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """форма регистрации нового пользователя"""
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

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


class CustomUserForm(UserChangeForm):
    """форма регистрации нового пользователя"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'country', 'avatar']
        exclude = ['password',]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']

        for field_name, field in self.fields.items():
            if field_name != 'avatar':
                field.widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя', })
        self.fields['phone'].widget.attrs.update({'placeholder': 'Телефон пользователя', })
        self.fields['country'].widget.attrs.update({'placeholder': 'Страна проживания', })

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, required=True, label='Имя', help_text='Введите ваше имя')
    last_name = forms.CharField(max_length=64, required=True, label='Фамилия', help_text='Введите вашу фамилию')
    patronymic = forms.CharField(max_length=64, required=False, label="Отчество")
    username = forms.CharField(
        max_length=32,
        required=True,
        label='Логин',
        help_text='Введите уникальный логин'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'password1', 'password2']

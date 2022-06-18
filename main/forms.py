from cProfile import label
from multiprocessing import AuthenticationError
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from .models import *

class OrderHouse(forms.Form):
    first_name = forms.CharField(max_length=32, label="Ім'я")
    last_name = forms.CharField(max_length=32, label='Прізвище')
    phone = forms.IntegerField(label='Телефон')
    email = forms.EmailField(label='Email')

    count_of_days = forms.IntegerField(max_value=5, min_value=1, label='Кількість днів')

    house = forms.ModelChoiceField(queryset=Houses.objects.all(), empty_label='Виберіть будинок', label='Будинок')
    # date_booking = forms.DateTimeField()
    date_future_settlment = forms.DateField(label='Дата поселення')
    # date_future_checkout = forms.DateField(label='Дата виселення')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
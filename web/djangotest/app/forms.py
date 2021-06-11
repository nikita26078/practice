from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput, Form
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper

from .models import ShipRequest, Employee, AdCampaign, FinanceReview, Item


class UserRegistrationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Повторите пароль', widget=PasswordInput)
    patronym = CharField(label='Отчество')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronym', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают.')
        return cd['password2']


class LoginForm(Form):
    username = CharField(label='Имя пользователя')
    password = CharField(label='Пароль', widget=PasswordInput)


class ShippingForm(ModelForm):
    class Meta:
        model = ShipRequest
        fields = ['shipper', 'items', 'desc']
        widgets = {
            'items': AddAnotherWidgetWrapper(
                forms.SelectMultiple,
                reverse_lazy('shipping_quantity'),
            ),
        }


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['post', 'phone']


class AdCampaignForm(ModelForm):
    class Meta:
        model = AdCampaign
        fields = ['title', 'plots', 'desc']


class FinanceReviewForm(ModelForm):
    class Meta:
        model = FinanceReview
        fields = ['title', 'plots', 'desc']


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'desc', 'category']

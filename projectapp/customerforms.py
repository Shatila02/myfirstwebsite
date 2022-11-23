from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction, models
from django import forms
from .models import *


class CustomerSignUpForm(UserCreationForm):
    phone_number = forms.IntegerField(min_value = 0, max_value = 9000000000000)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    address = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name' ,'username', 'email', 'password1', 'password2', 'phone_number', 'address']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username=self.cleaned_data.get('username')
        user.email=self.cleaned_data.get('email')
        user.phone_number=self.cleaned_data.get('phone_number')
        user.address=self.cleaned_data.get('address')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.first_name=self.cleaned_data.get('first_name')
        customer.last_name=self.cleaned_data.get('last_name')
        customer.username=self.cleaned_data.get('username')
        customer.email=self.cleaned_data.get('email')
        customer.phone_number=self.cleaned_data.get('phone_number')
        customer.address=self.cleaned_data.get('address')
        customer.save()
        return user

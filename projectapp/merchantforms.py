from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction, models
from django import forms
from .models import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    

class MerchantSignUpForm(UserCreationForm):
    phone_number = forms.IntegerField(min_value = 0, max_value = 9000000000000)
    company_name = forms.CharField(required = True)
    company_liscence = forms.CharField(required = True)
    company_location = forms.CharField(required = True)
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['company_name', 'company_liscence' ,'username', 'email','password1', 'password2', 'phone_number', 'company_location']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_merchant = True
        user.company_name = self.cleaned_data.get('company_name')
        user.company_liscence = self.cleaned_data.get('company_liscence')
        user.username=self.cleaned_data.get('username')
        user.email=self.cleaned_data.get('email')
        user.phone_number=self.cleaned_data.get('phone_number')
        user.company_location=self.cleaned_data.get('company_location')
        user.save()
        merchant = Merchant.objects.create(user=user)
        merchant.company_name=self.cleaned_data.get('company_name')
        merchant.company_liscence=self.cleaned_data.get('company_liscence')
        merchant.username=self.cleaned_data.get('username')
        merchant.email=self.cleaned_data.get('email')
        merchant.phone_number=self.cleaned_data.get('phone_number')
        merchant.company_location=self.cleaned_data.get('company_location')
        merchant.save()
        return user

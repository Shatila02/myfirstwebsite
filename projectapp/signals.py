"""from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from projectweb import settings

if 
#/accounts/google/login/
@receiver(post_save, sender = CustomUser)
def customer_create(sender, instance, created, *args, **kwargs):
    if created:
        instance.is_customer = True
        instance.save()
        customer = Customer.objects.create(user=instance)
        customer.username = instance.username
        customer.email = instance.email
        customer.first_name = instance.first_name
        customer.last_name = instance.last_name
        customer.save()
        print('ok:', settings.SOCIALACCOUNT_LOGIN_ON_GET)
"""
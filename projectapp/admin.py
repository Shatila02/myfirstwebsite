from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(SubCategories)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(About)
admin.site.register(Term)
admin.site.register(Contact)
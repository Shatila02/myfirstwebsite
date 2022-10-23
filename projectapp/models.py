from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name = 'customer', null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    profile_pic=models.FileField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username


class Merchant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    username = models.CharField(max_length=255)
    CEO = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    company_name = models.CharField(max_length=20)
    company_liscence = models.CharField(max_length=20)
    company_location = models.CharField(max_length=20)

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title
	


class SubCategories(models.Model):
    id=models.AutoField(primary_key=True)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)
    def get_absolute_url(self):
        return reverse("sub_category_list")



class Product(models.Model):
	id=models.AutoField(primary_key=True)
	url_slug=models.CharField(max_length=255)
	subcategories_id=models.ForeignKey(SubCategories,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=255, null=True)
	brand=models.CharField(max_length=255)
	max_price=models.DecimalField(max_digits=7, decimal_places=2)
	discount_price=models.DecimalField(max_digits=7, decimal_places=2)
	product_description=models.TextField()
	product_long_description=models.TextField()
	in_stock_total=models.IntegerField(default=1)
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	is_published = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.product_name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class ProductTags(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	order_status = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered'),
		)
	status = models.CharField(max_length=255, choices = order_status, default='Pending')

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.discount_price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

class WishList(models.Model):
	user = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

class OrderUpdate(models.Model):
	update_id = models.AutoField(primary_key=True)
	order_id =models.IntegerField(default=0, null=True, blank=True)
	update_desc = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.order_id 



class About(models.Model):
    about = models.TextField()
    def __str__(self):
        return str(self.about)
    def get_absolute_url(self):
        return reverse('admin')

class Term(models.Model):
    term = models.TextField()
    def __str__(self):
        return str(self.term)
    def get_absolute_url(self):
        return reverse('admin')

class Contact(models.Model):
    contact = models.TextField()
    def __str__(self):
        return str(self.contact)
    def get_absolute_url(self):
        return reverse('admin')


from django.shortcuts import render,redirect
from django.http import JsonResponse
import json, datetime
from .models import * 
from .customerforms import *
from .utils import cookieCart, cartData, guestOrder
from .models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .decorators import customer_required
from django.conf import settings
from django.urls import reverse

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'customertemplates/store.html', context)

@login_required(login_url="/customer_login/")
@customer_required
def category(request):
	data = cartData(request)

	cartItems = data['cartItems']

	category = Category.objects.all()
	context = {'category':category , 'cartItems':cartItems}
	return render(request, 'customertemplates/category.html', context)

@login_required(login_url="/customer_login/")
@customer_required
def subcategory(request, pk):
	data = cartData(request)

	cartItems = data['cartItems']
	category = Category.objects.get(id=pk)
	subcategory = SubCategories.objects.filter(category_id=category)
	context = {'subcategory':subcategory , 'cartItems':cartItems}
	return render(request, 'customertemplates/subcategory.html', context)

def subcategory_product(request, pk):
	data = cartData(request)

	cartItems = data['cartItems']
	subcategory = SubCategories.objects.get(id=pk)
	products = Product.objects.filter(subcategories_id=subcategory)
	context = {'products':products , 'cartItems':cartItems}
	return render(request, 'customertemplates/subcategory_products.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'customertemplates/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'customertemplates/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_customer:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)
		

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	print(order)
	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


@csrf_exempt
def loginCustomer(request):
    page = 'login'
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
		
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('customer_login')
    return render(request, 'account/login.html', {'page': page})

@csrf_exempt
def logoutCustomer(request):
    logout(request)
    return redirect('customer_login')

@csrf_exempt
def customerSignUpView(request):

    form_class = CustomerSignUpForm

    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('store')
    else:
        form = form_class()
    return render(request, 'customertemplates/register.html', {'form': form})

def productview(request, pk):
	product = Product.objects.get(id=pk)
	data = cartData(request)
	cartItems = data['cartItems']
	context = {
		'product': product, 'cartItems': cartItems
	}
	return render(request, 'customertemplates/product.html', context)

@csrf_exempt
@login_required(login_url='customer_login')
def wishlist(request):
	data = cartData(request)
	cartItems = data['cartItems']
	wishlist = WishList.objects.filter(user=request.user.customer)
	context = {
		'wishlist': wishlist, 'cartItems': cartItems,
	}
	return render(request, 'customertemplates/wishlist.html', context)

@csrf_exempt
def addwishlist(request):
	if request.method == 'POST':
		if request.user.is_authenticated:
			prod_id = int(request.POST.get('product_id'))
			product_check = Product.objects.get(id=prod_id)
			if(product_check):
				if(WishList.objects.filter(user=request.user.customer, product_id=prod_id)):
					return JsonResponse({'status':"Product already in wish list"})
				else:
					WishList.objects.create(user=request.user.customer, product_id=prod_id)
					return JsonResponse({'status':"Product added to wish list"})
			else:
				return JsonResponse({'status':"No such product exists"})
		else:
			return JsonResponse({'status':"Login to continue"})
	return redirect('/')

def deletewishlist(request):
	if request.method =="POST":
		if request.user.is_authenticated and request.user.is_customer:
			prod_id = int(request.POST.get('product_id'))
			if(WishList.objects.filter(user=request.user.customer, product_id=prod_id)):
				wishlistitem = WishList.objects.get(product_id=prod_id)
				wishlistitem.delete()
				return JsonResponse({'status':"Product removed from wish list"})
			else:
				return JsonResponse({'status':"Product not found in wish list"})
		else:
			return JsonResponse({'status':"Login to continue"})
	return redirect('wishlist')

def my_order(request):
	data = cartData(request)
	cartItems = data['cartItems']
	orders = Order.objects.filter(customer=request.user.customer)
	context = {'orders':orders, 'cartItems': cartItems,}
	return render(request, 'customertemplates/tracker.html', context)

def  orderview(request, t_no):
	data = cartData(request)
	cartItems = data['cartItems']
	order = Order.objects.filter(transaction_id=t_no).filter(customer=request.user.customer).first()
	orderitem = OrderItem.objects.filter(order=order)
	context = {'order':order, 'orderitem': orderitem, 'cartItems': cartItems,}
	return render(request, 'customertemplates/myorder.html', context)

def about(request):
	data = cartData(request)
	cartItems = data['cartItems']
	writeup = About.objects.all()
	context = {'writeup':writeup, 'cartItems': cartItems,}
	return render(request, 'customertemplates/about_us.html', context)

def term(request):
	data = cartData(request)
	cartItems = data['cartItems']
	writeup = Term.objects.all()
	context = {'writeup':writeup, 'cartItems': cartItems,}
	return render(request, 'customertemplates/terms.html', context)

def contact(request):
	data = cartData(request)
	cartItems = data['cartItems']
	writeup = Contact.objects.all()
	context = {'writeup':writeup, 'cartItems': cartItems,}
	return render(request, 'customertemplates/contact_us.html', context)



from django.urls import path

from . import customerviews

urlpatterns = [
	#Leave as empty string for base url
	path('', customerviews.store, name="store"),
    path('customer_login/', customerviews.loginCustomer, name="customer_login"),
    path('customer_logout/', customerviews.logoutCustomer, name="customer_logout"),
    path('customer_register/', customerviews.customerSignUpView, name="customer_signup"),
	path('cart/', customerviews.cart, name="cart"),
	path('checkout/', customerviews.checkout, name="checkout"),

	path('update_item/', customerviews.updateItem, name="update_item"),
	path('process_order/', customerviews.processOrder, name="process_order"),
	path('product_details/<int:pk>/', customerviews.productview, name="product_details"),
	path('wishlist/', customerviews.wishlist, name="wishlist"),
	path('add_wishlist', customerviews.addwishlist, name="add_wishlist"),
	path('delete-wishlist-item', customerviews.deletewishlist, name="deletewishlistitem"),
	path('my_orders', customerviews.my_order, name = "my_orders"),
	path('view_orders/<str:t_no>', customerviews.orderview, name = "orderview"),
	path('category', customerviews.category, name = "category"),
	path('subcategory/<int:pk>/', customerviews.subcategory, name = "subcategory"),
	path('about/', customerviews.about, name='about'),
	path('terms&policy/', customerviews.term, name='term'),
	path('contact/', customerviews.contact, name='contact'),
]

from django.urls import path
from django.conf.urls.static import static
from . import views, merchantviews
from django.conf import settings

urlpatterns = [
    path('merchant/', merchantviews.merchantLogin,name="merchant_login"),

    path('merchant_logout/',merchantviews.merchantLogout,name="merchant_logout"),
    
    path('merchantregister/', merchantviews.merchantSignUpView, name="merchant_signup"),

    # PAGE FOR merchant
    path('merchant_home/',merchantviews.merchant_home,name="merchant_home"),
    
    #CATEGORIES
    path('category_list',merchantviews.CategoriesListView.as_view(),name="category_list"),
    path('category_create',merchantviews.CategoriesCreate.as_view(),name="category_create"),
    path('category_update/<slug:pk>',merchantviews.CategoriesUpdate.as_view(),name="category_update"),
    

    #SUBCATEGORIES

    path('sub_category_list',merchantviews.SubCategoriesListView.as_view(),name="sub_category_list"),
    path('sub_category_create',merchantviews.SubCategoriesCreate.as_view(),name="sub_category_create"),
    path('sub_category_update/<slug:pk>',merchantviews.SubCategoriesUpdate.as_view(),name="sub_category_update"),

    #Products
    path('product_create',merchantviews.ProductView.as_view(),name="product_view"),
    path('product_list',merchantviews.ProductListView.as_view(),name="product_list"),
    path('product_edit/<str:product_id>',merchantviews.ProductEdit.as_view(),name="product_edit"),
    path('remove_product/<slug:pk>',merchantviews.Delete,name="remove_product"),

]
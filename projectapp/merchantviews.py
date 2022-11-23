from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View,DeleteView, TemplateView
from django.contrib.auth import authenticate,login,logout
from .models import Category,SubCategories,CustomUser,Merchant,Product, Customer
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .merchantforms import *
from .decorators import merchant_required
from django.http import JsonResponse


class SignUpView(TemplateView):
    template_name = 'commontemplates/usertypesignup.html'

@csrf_exempt
def merchantSignUpView(request):


    form_class = MerchantSignUpForm

    if request.method == 'POST':
        form = MerchantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('merchant_home')
    else:
        form = form_class()
    return render(request, 'merchanttemplates/register.html', {'form': form})

@csrf_exempt
def merchantLogin(request):
    page = 'signin'
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request=request,username=username,password=password)
        if user is not None and user.is_merchant == True:
            login(request,user)
            return redirect("merchant_home")
        else:
            messages.error(request,"Error in Login! Invalid Login Details!")
            return redirect("merchant_login")
    return render(request, 'merchanttemplates/signin.html', {'page': page})

@csrf_exempt
def merchantLogout(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return redirect("merchant_login")

@login_required(login_url="/merchant/")
@merchant_required
def merchant_home(request):
    return render(request,"merchanttemplates/home.html")

@method_decorator([login_required, merchant_required], name='dispatch')
class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Category
    success_message="Category Added!"
    fields="__all__"
    template_name="merchanttemplates/category_create.html"

@method_decorator([login_required, merchant_required], name='dispatch')
class CategoriesListView(ListView):
    model=Category
    template_name="merchanttemplates/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Category.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Category.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Category._meta.get_fields()
        return context



@method_decorator([login_required, merchant_required], name='dispatch')
class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Category
    success_message="Category Updated!"
    fields="__all__"
    template_name="merchanttemplates/category_update.html"


@method_decorator([login_required, merchant_required], name='dispatch')
class SubCategoriesListView(ListView):
    model=SubCategories
    template_name="merchanttemplates/sub_category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

@method_decorator([login_required, merchant_required], name='dispatch')
class SubCategoriesCreate(SuccessMessageMixin,CreateView):
    model=SubCategories
    success_message="Sub Category Added!"
    fields="__all__"
    template_name="merchanttemplates/sub_category_create.html"

@method_decorator([login_required, merchant_required], name='dispatch')
class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="merchanttemplates/sub_category_update.html"


@method_decorator([login_required, merchant_required], name='dispatch')
class ProductView(View):
    def get(self,request,*args,**kwargs):
        categories=Category.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        return render(request,"merchanttemplates/product_create.html",{"categories":categories_list})

    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        max_price=request.POST.get("max_price")
        discount_price=request.POST.get("discount_price")
        product_description=request.POST.get("product_description")
        product_long_description=request.POST.get("product_long_description")
        in_stock_total=request.POST.get("in_stock_total")
        product_tags=request.POST.get("product_tags")
        image = request.FILES['image']
        subcat_obj=SubCategories.objects.get(id=sub_category)
        product=Product(product_name=product_name,in_stock_total=in_stock_total,url_slug=url_slug,brand=brand,subcategories_id=subcat_obj,product_description=product_description,product_long_description=product_long_description,max_price=max_price,discount_price=discount_price, image=image)
        product.save()
                
        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        messages.success(request, 'Product added successfully')
        return HttpResponse("OK")

@method_decorator([login_required, merchant_required], name='dispatch')
class ProductCreate(SuccessMessageMixin,CreateView):
    model=Product
    success_message="Product Added!"
    fields="__all__"
    template_name="merchanttemplates/product_create.html"

@method_decorator([login_required, merchant_required], name='dispatch')
class ProductListView(ListView):
    model=Product
    template_name="merchanttemplates/product_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Product.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
            products=Product.objects.all().order_by(order_by)

        return products

    def get_context_data(self,**kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Product._meta.get_fields()
        return context

@method_decorator([login_required, merchant_required], name='dispatch')
class ProductEdit(View):

    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        product_tags=ProductTags.objects.filter(product_id=product_id)

        categories=Category.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        return render(request,"merchanttemplates/product_edit.html",{"categories":categories_list,"product":product,"product_tags":product_tags})

    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        max_price=request.POST.get("max_price")
        discount_price=request.POST.get("discount_price")
        in_stock_total=request.POST.get("in_stock_total")
        product_description=request.POST.get("product_description")
        product_tags=request.POST.get("product_tags")
        product_long_description=request.POST.get("product_long_description")
        image = request.FILES['image']
        subcat_obj=SubCategories.objects.get(id=sub_category)
        product_id=kwargs["product_id"]
        product=Product.objects.get(id=product_id)
        product.product_name=product_name
        product.image = image
        product.url_slug=url_slug
        product.brand=brand
        product.subcategories_id=subcat_obj
        product.product_description=product_description
        product.max_price=max_price
        product.discount_price= discount_price
        product.in_stock_total=in_stock_total
        product.product_long_description=product_long_description
        product.save()

        ProductTags.objects.filter(product_id=product_id).delete()

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        messages.success(request, 'Product updated successfully')
        
        return HttpResponse("OK")

@csrf_exempt
def Delete(request, pk):
    productremove = Product.objects.get(id=pk)
    productremove.delete()
    return redirect('product_list')



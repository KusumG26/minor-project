from django.shortcuts import render, redirect
from django.views import View
from .models import customer,productDetail,cart,orderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


class ProductView(View):
    def get(self,request):
        Boots = productDetail.objects.filter(category='b')
        Heels = productDetail.objects.filter(category='h')
        Sneakers = productDetail.objects.filter(category='s')
        return render(request, 'app/home.html', {'Boots':Boots, 'Heels':Heels, 'Sneakers':Sneakers})

class ProductDetailView(View):
    def get(self,request,pk):
        product = productDetail.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = productDetail.objects.get(id=product_id)
 cart(user=user,product=product).save()
 return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        Cart = cart.objects.filter(user=user)
        print(Cart)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.00
        cart_product = [p for p in cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
             temp_amount = (p.quantity * p.product.price)   
             amount += temp_amount
             totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':Cart , 'totalamount': totalamount, 'amount':amount})
        else:
         return render(request, 'app/emptycart.html')
      

def plus_cart(request):
        if request.user.is_authenticated:
          if request.method == 'GET':

            prod_id = request.GET['prod_id']
            c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity+=1
            c.save()
            amount = 0.0
            shipping_amount = 70.0
            cart_product = [p for p in cart.objects.all() if p.user == request.user]
            if cart_product:

             for p in cart_product:
              temp_amount = (p.quantity * p.product.price)   
              amount += temp_amount
              totalamount = amount + shipping_amount 

             data = {
                 'quantity': c.quantity,
                 'amount': amount,
                 'totalamount': totalamount
                }
             return JsonResponse(data)
            else:
             return render(request, 'app/emptycart.html')
             
def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 add = customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def Boots(request, data=None):
 if data == None:
  Boots = productDetail.objects.filter(category='b')
 return render(request, 'app/Boots.html',{'Boots':Boots})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Successfully registered ')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
        usr = request.user
        name= form.cleaned_data['name']
        address= form.cleaned_data['address']
        reg = customer(user=usr, name=name, address=address) 
        reg.save()
        messages.success(request,'Profile Updated Successfully')
      return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})
from django.shortcuts import render,HttpResponse, redirect 

from .models import *
from django.http import JsonResponse, request
import json

import datetime
from .utilis import CookieCart,cartData,guestOrder

#from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate, login, logout

# from django.contrib import messages
# from django.contrib.auth.decorators import login_require
# Create your views here.

# add registertration page 




def store(request):
     data = cartData(request)
     cartItem= data['cartItem']

     products = Product.objects.all()
     context = {'products':products,'cartItem':cartItem}
     return render(request,'store.html', context)

def cart(request):
     data = cartData(request)
     cartItem= data['cartItem']
     order= data['order']
     items= data['items']

     context = {'items':items,'order':order,'cartItem':cartItem}
     return render(request,'cart.html', context)

def checkout(request):
     data = cartData(request)
     cartItem= data['cartItem']
     order= data['order']
     items= data['items']

     context = {'items':items,'order':order,'cartItem':cartItem}

     return render(request, 'checkout.html', context)


def updateItem(request):
     data= json.loads(request.body)
     productId= data['productId']
     action = data['action']
     print('productId::',productId)
     print('action:',action)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order,created = Order.objects.get_or_create(customer=customer,complete=False)
     orderItem,created = Orderitem.objects.get_or_create(order=order,product=product)

     if(action=='add'):
          orderItem.quantity= (orderItem.quantity+1)
     
     elif(action=='remove'):
          orderItem.quantity= (orderItem.quantity-1)
     
     orderItem.save()

     if orderItem.quantity<=0:
          orderItem.delete()

     return JsonResponse('Item was added',safe=False)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     print('transaction_id',transaction_id)
     data = json.loads(request.body)
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=False)
            
     else:
          customer,order = guestOrder(request,data)
          
     total = float(data['form']['total'])  
     order.transaction_id= transaction_id

     #now let's check if user is not manupilate the data 
     if total == order.get_cart_total:
          order.complete=True
     order.save()
     
     if(order.shipping ==True):
          Shippingaddress.objects.create(
               customer=customer,
               order=order,
               address= data['shipping']['address'],
               city= data['shipping']['city'],
               state= data['shipping']['state'],
               zipcode= data['shipping']['zipcode'],
          )

     return JsonResponse('Payment submitted :)',safe=False)
     

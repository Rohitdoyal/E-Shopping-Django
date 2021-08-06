import json
from .models import *

def CookieCart(request):

    #for fix the tempary cookie type bug
    try:

        cart = json.loads(request.COOKIES['cart'])
    except:
        cart={}
    print('cart is :: ',cart)
    items=[]
    order={'get_cart_items':0,'get_cart_total':0,'shipping':False}
    cartItem = order['get_cart_items']

    for i in cart:
        try:
            cartItem=cartItem+cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price)*(cart[i]['quantity'])
            order['get_cart_total']=order['get_cart_total']+total
            order['get_cart_items']=order['get_cart_items']+cart[i]['quantity']

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total
                }
            items.append(item)
            if(product.digital ==False):
                order['shipping']= True
               
        except:
            pass
    return {'cartItem':cartItem,'order':order,'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookieData = CookieCart(request)
        cartItem =cookieData['cartItem']
        items = cookieData['items']
        order= cookieData['order']
    return {'cartItem':cartItem,'order':order,'items':items}


def guestOrder(request,data):
    print('user is not authenticated')
    print('Cookies ',request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = CookieCart(request)
    items = cookieData['items']
    customer,created = Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False
        )

          #add into data base so let's do it 
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = Orderitem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )

    return customer,order
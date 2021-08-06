from django.contrib import admin
from django.urls import path
from store import views 

urlpatterns = [

    
    path("",views.store,name='store'),
    path("cart/",views.cart, name= 'cart'),
    path("checkout/", views.checkout, name='checkout'),

    path("update_item/", views.updateItem, name='update_item'),
    path("process_order/", views.processOrder, name='process_order'),
    
    # path("login/", views.login, name='login'),
    # path("register/", views.register, name='register'),

]

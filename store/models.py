from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name= models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name= models.CharField(max_length=200,null=True)
    price= models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null = True,blank =True,default = "")
    def __str__(self):
        return self.name

    #if we don't have image case
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

#order relation product and customer
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_orderd =models.DateTimeField(auto_now_add=True)
    complete =   models.BooleanField(default=False,null=True,blank=False)
    transication_id = models.CharField(max_length=200,null=True)


    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitem= self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total
    
    @property
    def get_cart_items(self):
        orderitem= self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitem= self.orderitem_set.all()
        for i in orderitem:
            if(i.product.digital== False ):
                shipping = True
                break
        return shipping

#need to create orderitem card can have multiple order item 

class Orderitem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity =models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price*self.quantity 
        return total


class Shippingaddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address= models.CharField(max_length=200,null=True)
    city= models.CharField(max_length=200,null=True)
    state= models.CharField(max_length=200,null=True)
    zipcode= models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images',blank=True,null=True)
    description = models.TextField()

    def __str__(self):

        return self.name

class Product(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products',blank=True,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    created = models.DateTimeField(auto_now_add=True) #one time
    updated = models.DateTimeField(auto_now=True) # changes every time we update

    def __str__(self):
        return self.name

class Order_details(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_items = models.IntegerField()
    address = models.TextField()
    phone = models.BigIntegerField()
    pin = models.IntegerField()
    order_id = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30,default='pending')
    delivery_status = models.CharField(max_length=30,default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class Payment(models.Model):

    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=30)
    razorpay_payment_id  = models.CharField(max_length=30,blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id
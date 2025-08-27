from django.db import models

from shop.models import Product
from django.contrib.auth.models import User


# Create your models here.

class Cart(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="products")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    quantity = models.IntegerField()
    data_added = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price*self.quantity



    def __str__(self):
        return self.product.name
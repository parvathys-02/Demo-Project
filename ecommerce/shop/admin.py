from django.contrib import admin

# Register your models here.


from shop.models import Category, Product

from shop.models import Order_details

from shop.models import Payment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order_details)
admin.site.register(Payment)
from audioop import reverse

from django.shortcuts import render
from django.template.base import kwarg_re
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from shop.models import Category,Product

from shop.models import Order_details


# Create your views here.

class Home(ListView):

    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class ProductDetail(DetailView):

    model = Category
    template_name = 'product.html'
    context_object_name = 'category'

class Details(DetailView):

    model = Product
    template_name = 'details.html'
    context_object_name = 'pro'


class AddCategory(CreateView):

    model = Category
    template_name = 'add category.html'
    fields = ['name','image','description']
    success_url = reverse_lazy('shop:home')

class AddProduct(CreateView):

    model = Product
    template_name = 'add product.html'
    fields = ['name','image','description','price','stock','category']
    success_url = reverse_lazy('shop:home')

    # def get_success_url(self):     <!---for detail page (since id required to navigate to detail page) --->
    #     return reverse_lazy('shop:details',kwargs={'pk':self.object.id})


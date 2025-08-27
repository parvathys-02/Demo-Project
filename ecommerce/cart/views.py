from functools import total_ordering
from lib2to3.fixes.fix_input import context
from locale import currency

import razorpay

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart
from shop.models import Payment, Order_details


# Create your views here.

@login_required
def addtocart(request,i):
    user = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=user, product=p)
        if(p.stock>0):
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()

    except:
        if(p.stock>0):
            c = Cart.objects.create(user=user,product=p,quantity=1)
            c.save()
            p.stock-=1
            p.save()

    return redirect('cart:cartview')

@login_required
def cartview(request):

    u = request.user
    c = Cart.objects.filter(user=u)

    total = 0
    for i in c:
        total += i.quantity*i.product.price

    context = {'cart':c,'total':total}

    return render(request,'cart.html',context)

@login_required
def cart_minus(request,i):
    user = request.user
    p = Product.objects.get(id=i)
    c = Cart.objects.get(user=user, product=p)
    if(c.quantity>1):
        c.quantity-=1
        c.save()
        p.stock+=1
        p.save()
    else:
        c.delete()
        p.stock += 1
        p.save()
    return redirect('cart:cartview')


@login_required
def cart_delete(request,i):
    user = request.user
    p = Product.objects.get(id=i)
    c = Cart.objects.get(user=user, product=p)
    c.delete()
    p.stock += c.quantity
    p.save()

    return redirect('cart:cartview')

def orderform(request):

    if(request.method=="POST"):

        a = request.POST['a']
        pn = request.POST['p']
        n = request.POST['pin']

        user = request.user
        c = Cart.objects.filter(user=user)

        total = 0

        for i in c:

            total = total+ (i.quantity*i.product.price)
        total = int(total)   #decimalfield given in model

        #Razorpay client connection
        client = razorpay.Client(auth=('rzp_test_RXnkeyGg823dFS','inPYhnb9QFq1jGqXT3r7kDM1'))

        #Razorpay order creation
        response_payment = client.order.create(dict(amount=total*100,currency='INR'))

        print(response_payment)

        #retrieving order_id and status from response payment
        order_id = response_payment['id']
        status = response_payment['status']

        if(status=="created"):

            p = Payment.objects.create(name=user.username,amount=total,order_id=order_id)
            p.save()

            for i in c:

                o = Order_details.objects.create(product = i.product,user = i.user,phone=pn,address = a,pin = n,order_id=order_id,no_of_items=i.quantity)
                o.save()

            context = {'payment':response_payment,'name':user.username}  #sends the response from view to payment.html


            return render(request,'payment.html',context)


    return render(request,'orderform.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_status(request,p):

    user = User.objects.get(username=p)
    login(request,user)

    response = request.POST
    print(response)

    #TO CHECK THE VALIDITY (AUTHENTICITY) OF RAZORPAY PAYMENT DETAILS RECEIVED BY APPLICATION

    param_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    client = razorpay.Client(auth=('rzp_test_RXnkeyGg823dFS','inPYhnb9QFq1jGqXT3r7kDM1'))

    try:
        status = client.utility.verify_payment_signature(param_dict)
        print(status)
        p = Payment.objects.get(order_id=response['razorpay_order_id'])
        p.paid = True
        p.razorpay_payment_id = response['razorpay_payment_id']
        p.save()

        o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:

            i.payment_status = 'completed'
            i.save()

        c = Cart.objects.filter(user = user)
        c.delete()

    except:
         pass


    return render(request,'payment-status.html')

def yourorders(request):

    user = request.user
    o = Order_details.objects.filter(user=user,payment_status="completed")
    context = {'orders':o}
    return render(request,'yourorders.html',context)



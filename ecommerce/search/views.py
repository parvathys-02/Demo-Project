from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.db.models import Q
from shop.models import Product
from django.contrib.auth.decorators import login_required

def search(request):
    products = []
    if request.method == "POST":
        query = request.POST.get('q', '')
        products = Product.objects.filter(Q(name__icontains=query))

    return render(request, 'search.html', {'product': products})


def searchdetail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'searchdetail.html', {'product': product})

def register(request):

    if (request.method=="POST"):

        u = request.POST['user']
        p = request.POST['pass']
        p1 = request.POST['pass1']
        e = request.POST['email']
        f = request.POST['first']
        l = request.POST['last']

        if (p==p1):
            user = User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            user.save()
            return redirect('shop:home')
        else:

            messages.error(request,"Passwords does not match")

    return render(request,'register.html')

def user_login(request):
    if(request.method=="POST"):

        u = request.POST.get('user')
        p = request.POST.get('pass')

        user = authenticate(username=u,password=p)

        if user:
            login(request,user)
            return redirect('shop:home')
        else:
            messages.error(request,"Invalid Credentials")


    return render(request,'login.html')


@login_required
def user_logout(request):

    logout(request)

    return redirect('shop:home')



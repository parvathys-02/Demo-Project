from lib2to3.fixes.fix_input import context

from .models import Cart

def count_items(request):
    count = 0
    u = request.user
    if request.user.is_authenticated:
       c = Cart.objects.filter(user=u)


       for i in c:
           count += i.quantity



    return {'count':count}



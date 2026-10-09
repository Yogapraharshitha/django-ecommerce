from django.shortcuts import render
from .models import Products

# Create your views here.
def product_list(request):
    products=Products.objects.all()
    context={
        'products':products
    }
    return render(request,'product_list.html',context)

def product_details(request,id):
    product=Products.objects.get(id=id)   
    context={
        'product':product

    }
    return render(request,'product_detail.html',context)

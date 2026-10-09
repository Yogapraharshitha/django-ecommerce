from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Products


def product_list(request):
    query = request.GET.get('q', '').strip()
    products = Products.objects.all().order_by('-id')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'product_list.html', context)


def product_details(request, id):
    product = get_object_or_404(Products, id=id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

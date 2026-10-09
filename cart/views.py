from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Products
from .models import Cart, CartItems


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.stock < 1:
        messages.warning(request, 'Out of stock')
        return redirect('cart')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItems.objects.get_or_create(
        cart=cart, products=product, defaults={'quantity': 0}
    )
    cart_item.quantity += 1
    cart_item.save()

    product.stock -= 1
    product.save()

    messages.success(request, f'{product.name} added to cart')
    return redirect('cart')


@login_required(login_url='login')
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItems.objects.filter(cart=cart).select_related('products')

    total = 0
    for item in cart_items:
        item.subtotal = item.products.price * item.quantity
        total += item.subtotal

    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    })


@login_required(login_url='login')
@require_POST
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    product = cart_item.products

    if product.stock < 1:
        messages.warning(request, 'Out of stock')
        return redirect('cart')

    cart_item.quantity += 1
    cart_item.save()

    product.stock -= 1
    product.save()
    return redirect('cart')


@login_required(login_url='login')
@require_POST
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    product = cart_item.products

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    product.stock += 1
    product.save()
    return redirect('cart')


@login_required(login_url='login')
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItems, id=item_id, cart__user=request.user)
    product = cart_item.products

    product.stock += cart_item.quantity
    product.save()

    cart_item.delete()
    return redirect('cart')
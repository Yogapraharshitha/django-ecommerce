from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Cart, CartItems
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Orders, OrderItems
from products.models import Products
from django.db.models import F


@login_required(login_url="login")
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItems.objects.filter(cart=cart).select_related('products')

    if not cart_items.exists():
        messages.error(request, 'cart is empty')
        return redirect('cart')

    # No stock check here: stock was already reserved when items were added to the cart
    total = sum(item.products.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'checkout.html', context)


@login_required(login_url="login")
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItems.objects.filter(cart=cart).select_related('products')

    if not cart_items.exists():
        messages.error(request, 'cart is empty')
        return redirect('cart')

    total = 0
    for item in cart_items:
        total += item.products.price * item.quantity

    order = Orders.objects.create(
        user=request.user,
        total_amount=total,
        status='pending'
    )

    for item in cart_items:
        OrderItems.objects.create(
            order=order,
            product=item.products,
            price=item.products.price,
            quantity=item.quantity
        )

    cart_items.delete()
    messages.success(request, 'Order placed successfully')
    return redirect('my_orders')


@login_required(login_url='login')
def my_orders(request):
    orders = (
        Orders.objects
        .filter(user=request.user)
        .prefetch_related("orderitems_set__product")
        .order_by("-created_at")
    )
    return render(request, "my_orders.html", {"orders": orders})


@login_required(login_url='login')
def order_detail(request, id):
    order = get_object_or_404(Orders, id=id, user=request.user)
    order_items = (
        OrderItems.objects
        .filter(order=order)
        .select_related('product')
        .annotate(subtotal=F('price') * F('quantity'))
    )
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_detail.html', context)
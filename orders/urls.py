from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path("my_orders/", views.my_orders, name="my_orders"),
    path('order_detail/<int:id>/', views.order_detail, name='order_detail'),
]

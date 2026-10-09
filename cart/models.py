from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)



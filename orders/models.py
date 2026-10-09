from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status_choices=[
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('shipped','shipped'),
        ('dilvered','delivered'),
        ('canceled','canceled')
    ]
    status=models.CharField(choices=status_choices)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItems(models.Model):
    order=models.ForeignKey(Orders,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.PROTECT)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    quantity=models.PositiveIntegerField()

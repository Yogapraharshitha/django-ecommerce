from django.db import models

# Create your models here.
class Products(models.Model):
    name=models.CharField()
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/')
    category=models.CharField()
    
    def __str__(self):
        return self.name
    
    


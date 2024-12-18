from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Cake(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    img=models.FileField()
    quantity=models.TextField()
    colour=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE) 
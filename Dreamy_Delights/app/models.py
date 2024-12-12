from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CupCake(models.Model):
    id=models.TextField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    img=models.FileField()
    category=models.TextField()
    quantity=models.IntegerField()
    description=models.TextField()

class LayerCake(models.Model):
    id=models.TextField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    img=models.FileField()
    category=models.TextField()
    colour=models.TextField()
    quantity=models.IntegerField()
    description=models.TextField()  

class OneTierCake(models.Model):
    id=models.TextField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    img=models.FileField()
    category=models.TextField()
    colour=models.TextField()
    quantity=models.IntegerField()
    description=models.TextField() 

class TwoTierCake(models.Model):
    id=models.TextField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    img=models.FileField()
    category=models.TextField()
    colour=models.TextField()
    quantity=models.IntegerField()
    description=models.TextField()             
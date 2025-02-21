from django.db import models
from django.contrib.auth.models import User
from .constants import PaymentStatus
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

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

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)    


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.IntegerField()
    status=CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False,blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"),max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_address=models.ForeignKey(Address, on_delete=models.SET_NULL,null=True,blank=True)
       
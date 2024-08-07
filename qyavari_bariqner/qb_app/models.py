from django.contrib.auth.models import User
from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='images/')
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



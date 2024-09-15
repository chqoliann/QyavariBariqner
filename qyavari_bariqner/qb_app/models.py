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

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cart}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    liked_products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250)
    items = models.ManyToManyField(CartItem)


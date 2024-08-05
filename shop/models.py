from django.contrib.auth.models import User
from django.db import models

from leatherShop import settings


# Create your models here.


class Bag(models.Model):
    name = models.CharField('Название сумки', max_length=200)
    description = models.CharField('Описание', max_length=500)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.name


class BagImage(models.Model):
    bag = models.ForeignKey(Bag, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фотографии сумки', upload_to='images/bag_images')

    def __str__(self):
        return f"{self.bag.name} Image"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Используем модель User напрямую
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Bag, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"

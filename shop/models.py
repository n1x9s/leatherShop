from django.contrib.auth.models import User
from django.db import models


class Bag(models.Model):
    name = models.CharField('Название сумки', max_length=200)
    description = models.CharField('Описание', max_length=500)
    price = models.IntegerField('Цена')
    discount = models.PositiveSmallIntegerField('Скидка', default=0)

    def discounted_price(self):
        return self.price * (100 - self.discount) / 100

    def __str__(self):
        return self.name


class BagImage(models.Model):
    bag = models.ForeignKey(Bag, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фотографии сумки', upload_to='images/bag_images')

    def __str__(self):
        return f"{self.bag.name} Image"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Bag, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Почта')
    phone = models.CharField('Номер телефона', max_length=20)
    address = models.CharField('Адрес', max_length=255)
    comment = models.TextField('Комментарий', blank=True, null=True)
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Bag, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество')

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"

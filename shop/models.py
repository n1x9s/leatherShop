from django.db import models


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

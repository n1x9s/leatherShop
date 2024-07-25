from django.db import models


# Create your models here.


class Bag(models.Model):
    image = models.ImageField('Фотография сумки', upload_to='images/bag_images')
    name = models.CharField('Название сумки', max_length=200)
    description = models.CharField('Описание', max_length=500)
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.name

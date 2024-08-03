from django.contrib import admin
from .models import Bag, BagImage


class BagImageInline(admin.TabularInline):
    model = BagImage
    extra = 3


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [BagImageInline]

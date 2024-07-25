from django.shortcuts import render
from .models import Bag


# Create your views here.


def index(request):
    return render(request, 'shop/index.html', {'bags': Bag.objects.all()})


def detail(request):
    return render(request, 'shop/detail.html')

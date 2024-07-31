from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Bag


# Create your views here.


class Index(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'bags'
    model = Bag


class Detail(DetailView):
    template_name = 'shop/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Bag, pk=self.kwargs['id_bag'])

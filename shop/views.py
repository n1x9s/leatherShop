from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .models import Bag, Cart, CartItem


# Create your views here.


class Index(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'bags'
    model = Bag


class Detail(DetailView):
    template_name = 'shop/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Bag, pk=self.kwargs['id_bag'])


# test
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Bag, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop:cart_detail')
    else:
        return redirect('shop:bag_list')


def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items})


def remove_item_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('shop:cart_detail')
    else:
        return redirect('shop:cart_detail')


def remove_all_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect('shop:cart_detail')
    else:
        return redirect('shop:cart_detail')

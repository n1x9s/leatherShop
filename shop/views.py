from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Bag, Cart, CartItem, Order, OrderItem
from .forms import OrderForm


class Index(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'bags'
    model = Bag
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('discount'):
            queryset = queryset.filter(discount__gt=0)

        price_order = self.request.GET.get('price_order')
        if price_order == 'price_asc':
            queryset = queryset.order_by('price')
        elif price_order == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_filter'] = {
            'discount': self.request.GET.get('discount', ''),
            'price_order': self.request.GET.get('price_order', '')
        }
        return context


class Detail(DetailView):
    template_name = 'shop/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Bag, pk=self.kwargs['id_bag'])


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Bag, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop:cart_detail')
    else:
        return redirect('shop:index')


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


def search(request):
    query = request.GET.get('q')
    if query:
        bags = Bag.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        bags = Bag.objects.all()
    return render(request, 'shop/search_results.html', {'bags': bags, 'query': query})


@login_required
def order_bag(request, product_id):
    product = get_object_or_404(Bag, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1
            )

            return redirect('shop:order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'shop/order_form.html', {'form': form, 'product': product})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

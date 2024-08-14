from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Bag, Cart, CartItem, Order, OrderItem
from .forms import OrderForm, BagForm


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


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_sum = sum(item.product.discounted_price() * item.quantity for item in cart_items)

    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_sum': total_sum})


@login_required
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


@login_required
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
        bags = Bag.objects.filter(Q(name__icontains=query) | Q(description__icontains(query)))
    else:
        bags = Bag.objects.all()
    return render(request, 'shop/search_results.html', {'bags': bags, 'query': query})


@login_required
def order_form(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            cart_items.delete()  # Очищаем корзину после оформления заказа
            return redirect('shop:order_success', order_id=order.id)
    else:
        form = OrderForm()

    total_sum = sum(item.product.discounted_price() * item.quantity for item in cart_items)

    return render(request, 'shop/order_form.html', {'form': form, 'total_sum': total_sum})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'shop/admin_panel.html')


@user_passes_test(is_admin)
def admin_bag_list(request):
    bags = Bag.objects.all()
    return render(request, 'shop/admin_bag_list.html', {'bags': bags})


@user_passes_test(is_admin)
def admin_bag_edit(request, bag_id=None):
    if bag_id:
        bag = get_object_or_404(Bag, id=bag_id)
    else:
        bag = Bag()

    if request.method == 'POST':
        form = BagForm(request.POST, instance=bag)
        if form.is_valid():
            form.save()
            return redirect('shop:admin_bag_list')
    else:
        form = BagForm(instance=bag)

    return render(request, 'shop/admin_bag_edit.html', {'form': form})


@user_passes_test(is_admin)
def admin_bag_delete(request, bag_id):
    bag = get_object_or_404(Bag, id=bag_id)
    if request.method == 'POST':
        bag.delete()
        return redirect('shop:admin_bag_list')
    return render(request, 'shop/admin_bag_delete_confirm.html', {'bag': bag})


@user_passes_test(is_admin)
def admin_order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/admin_order_list.html', {'orders': orders})

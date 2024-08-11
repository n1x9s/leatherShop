from django import forms
from .models import Order, Bag


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'comment']


class BagForm(forms.ModelForm):
    class Meta:
        model = Bag
        fields = ['name', 'description', 'price', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})




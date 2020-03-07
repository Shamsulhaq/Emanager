from django import forms
from orders.models import Order


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = (
            'status',)

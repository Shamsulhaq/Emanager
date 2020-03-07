from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.messages.views import messages
# Create your views here.

from services.models import Service
from .forms import CreateOrder
from .models import Order
from accounts.forms import LoginForm



def create_order(request, id):
    form = CreateOrder(request.POST or None)
    user_form = LoginForm()
    service = get_object_or_404(Service, id=id)
    print(service)
    if form.is_valid():
        obj = Order()
        obj.short_note = form.cleaned_data.get("short_note")
        obj.address_line_1 = form.cleaned_data.get("address_line_1")
        obj.city = form.cleaned_data.get("city")
        obj.postal_code = form.cleaned_data.get("postal_code")
        obj.service = service
        obj.customer = request.user
        obj.save()
        messages.success(request, "Your Hire Order Create Successfully!")
        return redirect('index')

    return render(request, 'service/order.html', {'login_form': user_form, 'form': form})


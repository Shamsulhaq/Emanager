from django.contrib.messages.views import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order,OrderItem
from .forms import OrderStatusForm


@login_required
def index(request):
    if request.user.is_staff:
        order_obj = Order.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(order_obj, 20)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)

        context = {
            'object': order
        }
        return render(request, 'control_panel/index.html', context)
    return redirect('dashboard_home')


@login_required
def done_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='shipped')
        page = request.GET.get('page', 1)

        paginator = Paginator(order_obj, 20)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        context = {
            'object': order
        }
        return render(request, 'control_panel/index.html', context)
    return redirect('dashboard_home')


@login_required
def on_process_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='paid')
        page = request.GET.get('page', 1)

        paginator = Paginator(order_obj, 20)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        context = {
            'object': order
        }
        return render(request, 'control_panel/index.html', context)
    return redirect('dashboard_home')


@login_required
def pending_order(request):
    if request.user.is_staff:
        order_obj = Order.objects.filter(status='submit')
        page = request.GET.get('page', 1)

        paginator = Paginator(order_obj, 20)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        context = {
            'object': order
        }
        return render(request, 'control_panel/index.html', context)
    return redirect('dashboard_home')


# Search View
@login_required
def search_order(request):
    if request.user.is_staff:
        search = request.GET.get('q')
        if search:
            order_obj = Order.objects.filter(
                Q(order_id__icontains=search))
        page = request.GET.get('page', 1)

        paginator = Paginator(order_obj, 20)
        try:
            order = paginator.page(page)
        except PageNotAnInteger:
            order = paginator.page(1)
        except EmptyPage:
            order = paginator.page(paginator.num_pages)
        context = {
            'object': order
        }
        return render(request, 'control_panel/index.html', context)
    return redirect('dashboard_home')


@login_required
def single_order(request, id):
    if request.user.is_staff:
        object = Order.objects.get(id=id)
        cart_obj = OrderItem.objects.filter(order=object)
        form = OrderStatusForm(request.POST or None, request.FILES or None, instance=object)
        if form.is_valid():
            instance = form.save()
            instance.save()
            messages.success(request, 'Order Update Successfully')

        context = {
            'obj': object,
            'form':form,
            'cart_obj':cart_obj
        }
        return render(request, 'control_panel/single_order.html', context)
    return redirect('dashboard_home')


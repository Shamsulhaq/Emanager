from django.contrib.messages.views import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manager.models import Order


@login_required
def dashboard(request):
    user = request.user
    pending_order_obj = Order.objects.get_all_pending(user)
    order_obj = Order.objects.get_all_order(user)
    on_process_order = Order.objects.get_order_paid(user)
    done_order_obj = Order.objects.get_all_done(user)
    context = {
        'done_order_obj': done_order_obj,
        'on_process_order': on_process_order,
        'pending_order_obj': pending_order_obj,
        'billing_obj': user,
        'order_obj': order_obj,
    }
    return render(request, 'dashboard/home.html', context)



@login_required
def on_process_order(request):
    user = request.user
    order_obj = Order.objects.get_order_paid(user)
    page = request.GET.get('page', 1)

    paginator = Paginator(order_obj, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    context = {

        'object': order,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def all_order(request):
    user = request.user
    order_obj = Order.objects.get_all_order(user)
    page = request.GET.get('page', 1)

    paginator = Paginator(order_obj, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    context = {
        'object': order,
    }
    return render(request, 'dashboard/order.html', context)




@login_required
def done_order(request):
    user = request.user
    order_obj = Order.objects.get_all_done(user)
    page = request.GET.get('page', 1)

    paginator = Paginator(order_obj, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    context = {
        'object': order,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def pending_order(request):
    user = request.user
    order_obj = Order.objects.get_all_pending(user)
    page = request.GET.get('page', 1)

    paginator = Paginator(order_obj, 15)
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    context = {
        'object': order,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def order_info_view(request, id):
    user = request.user
    object = Order.objects.get(id=id)
    context = {
        'obj': object,
    }
    if user.is_authenticated:
        return render(request, 'dashboard/order.html', context)
    return redirect('login-url')

#
# @login_required
# def address_book(request):
#     user = request.user
#     billing_obj = get_object_or_404(BillingProfile, user=user, active=True)
#     qs = Address.objects.filter(billing_profile=billing_obj, active=True)
#     address_obj = qs
#     return render(request, 'dashboard/address_book.html', {'address_obj': address_obj})
#
#
@login_required
def account_info(request):
    user = request.user
    return render(request, 'dashboard/account_info.html', {'object': user})




# # Rent Section
#
# @login_required
# def all_rent(request):
#     user = request.user
#     rent_obj = Rent.objects.get_all_rent(user)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(rent_obj, 15)
#     try:
#         order = paginator.page(page)
#     except PageNotAnInteger:
#         order = paginator.page(1)
#     except EmptyPage:
#         order = paginator.page(paginator.num_pages)
#     context = {
#         'object': order,
#     }
#     return render(request, 'dashboard/rent.html', context)
#
#
# @login_required
# def done_rent(request):
#     user = request.user
#     order_obj = Rent.objects.get_all_done(user)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(order_obj, 15)
#     try:
#         order = paginator.page(page)
#     except PageNotAnInteger:
#         order = paginator.page(1)
#     except EmptyPage:
#         order = paginator.page(paginator.num_pages)
#     context = {
#         'object': order,
#     }
#     return render(request, 'dashboard/rent.html', context)
#
#
# @login_required
# def pending_rent(request):
#     user = request.user
#     order_obj = Rent.objects.get_all_pending(user)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(order_obj, 15)
#     try:
#         order = paginator.page(page)
#     except PageNotAnInteger:
#         order = paginator.page(1)
#     except EmptyPage:
#         order = paginator.page(paginator.num_pages)
#     context = {
#         'object': order,
#     }
#     return render(request, 'dashboard/rent.html', context)
#
#
# @login_required
# def return_rent(request):
#     user = request.user
#     order_obj = Rent.objects.get_all_return(user)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(order_obj, 15)
#     try:
#         order = paginator.page(page)
#     except PageNotAnInteger:
#         order = paginator.page(1)
#     except EmptyPage:
#         order = paginator.page(paginator.num_pages)
#     context = {
#         'object': order,
#     }
#     return render(request, 'dashboard/rent.html', context)
#
#
# @login_required
# def rent_info_view(request, id):
#     user = request.user
#     object = Rent.objects.get(id=id)
#     context = {
#         'obj': object,
#     }
#     if user.is_authenticated:
#         return render(request, 'dashboard/rent.html', context)
#     return redirect('login-url')

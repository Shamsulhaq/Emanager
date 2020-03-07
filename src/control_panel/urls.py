from django.urls import path
from .views import index, single_order,done_order,on_process_order,pending_order,search_order

urlpatterns = [
    path('cp/admin/',index, name='order_admin_index_url'),
    path('cp/admin/search/', search_order, name='search_order'),
    path('cp/admin/done/', done_order, name='done_order_url'),
    path('cp/admin/on-process/', on_process_order, name='admin_process_order_url'),
    path('cp/admin/pending/', pending_order, name='pending_order_url'),
    path('cp/admin/order_info/<id>', single_order, name='order_admin_single_order_url'),
    ]
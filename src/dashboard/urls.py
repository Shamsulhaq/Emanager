from django.urls import path
from .views import dashboard, all_order, order_info_view, done_order, pending_order, on_process_order,account_info
urlpatterns = [
    path('db/', dashboard, name='dashboard_home'),
    path('db/account/', account_info, name='db-account-url'),
    path('order/on-process', on_process_order, name='on-process-order-view-url'),
    path('order/all/', all_order, name='all-order-view-url'),
    path('order/pending/', pending_order, name='pending-order-view-url'),
    path('order/done/', done_order, name='done-order-view-url'),
    path('order/order_info/<id>', order_info_view, name='order-info-view-url'),
]

from django.contrib import admin
from .models import Order


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'service', 'customer', 'expert', 'address_line_1', 'price', 'status',
                    'timestamp', 'active']
    search_fields = ['order_id', 'status']
    # filter_vertical = ['category']
    list_per_page = 25
    list_filter = ['price', 'status', 'active', 'timestamp', 'expert']

    class Meta:
        Model = Order


admin.site.register(Order, OrderAdmin)

from django.contrib import admin
from .models import Category, Service


# Register your models here.


class ServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'get_discount',
                    'timestamp', 'active', 'slug']
    search_fields = ['descriptions', 'name']
    filter_vertical = ['category']
    list_per_page = 25
    list_filter = ['price', 'category', 'active', 'timestamp']

    class Meta:
        Model = Service


admin.site.register(Service, ServicesAdmin)
admin.site.register(Category)


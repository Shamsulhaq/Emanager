from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from services.models import Service, Category


class ServiceList(DetailView):
    template_name = 'service/servicelist.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceList, self).get_context_data(*args, **kwargs)
        obj = Service.objects.get_by_category(self.object)
        context['object_list'] = obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Category.objects.get_by_slug(slug)
        if instance is None:
            raise Http404("Page not found")
        return instance


class ServiceDetails(DetailView):
    template_name = 'service/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceDetails, self).get_context_data(*args, **kwargs)
        # context['title'] = '{}'.format(self.get_object().title)
        # context['cart_product_form'] = CartAddProductForm()
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Service.objects.get_by_slug(slug=slug)
        if instance is None:
            raise Http404("Page not found")
        return instance

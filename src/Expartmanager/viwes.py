from django.views.generic import ListView
from services.models import Category,Service


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        # obj = Service.objects.get_by_category(self.object)
        # counts = obj.count()
        # context['counts'] = counts
        return context

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()

# class SearchView(ListView):
#     template_name = 'search/search_view.html'
#     paginate_by = 20
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(SearchView, self).get_context_data(*args, **kwargs)
#         context['query'] = self.request.GET.get('q')
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         query = self.request.GET.get('q', None)
#         if query is not None:
#             return BookList.objects.search(query)
#         else:
#             return BookList.objects.is_stock()

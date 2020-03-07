import os
import random
from Expartmanager.utils import unique_slug_generator
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse

fs = FileSystemStorage(location='media')


# To get extension from upload file
def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Book image with new name by function
def upload_service_image_path(inistance, file_name):
    service_name = slugify(inistance.name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"service/service/{service_name}/{final_filename}"


def upload_category_image_path(inistance, file_name):
    service_name = slugify(inistance.keyword)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"service/category/{service_name}/{final_filename}"


class CategoryManager(models.Manager):
    def get_category(self):
        return self.get_queryset().all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            instance = qs.first()
        return instance


class Category(models.Model):
    keyword = models.CharField(max_length=155, help_text='Enter Tag keyword', unique=True)
    image = models.ImageField(upload_to=upload_category_image_path, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['keyword']

    objects = CategoryManager()

    @property
    def title(self):
        return self.keyword

    def get_count(self):
        qs = Service.objects.filter(category__keyword=self.keyword).count()
        print(qs)
        return qs


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_pre_save_receiver, sender=Category)


class ServiceQuerySet(models.query.QuerySet):
    def active(self):  # for check is Activ
        return self.filter(active=True)

    def search(self, keyword):
        lookups = (
                Q(name__icontains=keyword) |
                Q(descriptions__icontains=keyword) |
                Q(category__keyword__icontains=keyword))

        return self.active().filter(lookups).distinct()


class ServiceManager(models.Manager):
    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return qs

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def search(self, query):
        return self.get_queryset().search(keyword=query)

    def get_by_category(self, category):
        qs = self.get_queryset().filter(category=category)
        return qs


class Service(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=255, help_text="Enter service title")
    image = models.ImageField(upload_to=upload_service_image_path, blank=True)
    regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descriptions = models.TextField(blank=True, null=True)
    orders = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ServiceManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    def get_discount(self):
        if self.regular_price == 0:
            discount = None
            return discount
        else:
            discount = (self.regular_price - self.price) / self.regular_price * 100
            discount = int(discount)
            return str(discount) + '%'

    def get_absolute_url(self):
        return reverse('service-details-view-url', kwargs={'slug': self.slug})


def book_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(book_slug_pre_save_receiver, sender=Service)

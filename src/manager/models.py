import os
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.db import models
from services.models import Service
from person.models import Expert
from Expartmanager.utils import unique_order_id_generator

User = settings.AUTH_USER_MODEL

# Create your models here.
STATUS_CHOICES = (
    ('create', 'Create'),
    ('pending', 'Pending'),
    ('confirm', 'Confirm'),
    ('ongoing', 'OnGoing'),
    ('completed', 'Completed'),
    ('rated', 'Rated'),
    ('cancel', 'Cancel')

)


class OrderManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()

    def get_by_order_id(self, id):
        qs = self.get_queryset().filter(order_id=id)
        if qs.count() == 1:
            return qs.first()

    # for User
    def get_order_paid(self, customer):
        qs = self.get_queryset().filter(customer=customer, status='paid') | self.get_queryset().filter(
            customer=customer, status='confirm')
        return qs

    def get_all_order(self, customer):
        qs = self.get_queryset().filter(customer=customer)
        if qs.count() == 1:
            return qs
        return qs

    def get_all_pending(self, customer):
        qs = self.get_queryset().filter(customer=customer, status='Pending') | self.get_queryset().filter(
            customer=customer, status='create')
        return qs

    def get_all_done(self, customer):
        qs = self.get_queryset().filter(customer=customer, status='rated') | self.get_queryset().filter(
            customer=customer, status='completed')
        return qs


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, blank=True, null=True)
    short_note = models.TextField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=255)
    city = models.CharField(max_length=120, default='Dhaka')
    postal_code = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Bangladesh')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    status = models.CharField(max_length=120, default='create', choices=STATUS_CHOICES)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.order_id

    def update_price(self):
        self.price = self.service.price
        return self.price

    def order_count(self):
        service = Service.objects.get_by_id(self.service.id)
        service.orders += 1
        service.save()

    def cancel_order(self):
        service = Service.objects.get_by_id(self.service.id)
        service.status = 'cancel'
        service.save()

    def get_address(self):
        return "{address1}\n{city}\n{postal}\n{country}".format(
            address1=self.address_line_1,
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )


def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    if not instance.price:
        instance.update_price()

    if instance.status == 'confirm':
        instance.order_count()

    if instance.status == 'rated':
        instance.active = False

    # if instance.status == 'submit':
    #     pk = instance.id
    #     object = Order.objects.filter(id=pk)
    #     text = {
    #         'object': object,
    #     }
    #     print(object)
    #     print(text)
    #     mail_subject = 'Payment Successful'
    #     message = get_template('carts/success.html').render(text)
    #     to_email = instance.billing_profile.email
    #     email_from = settings.EMAIL_HOST_USER
    #     email = EmailMessage(
    #         mail_subject, message, email_from, to=[to_email]
    #     )
    #     email.content_subtype = 'html'
    #     print(to_email)
    #     email.send()


pre_save.connect(pre_save_order_id_receiver, sender=Order)
# def post_save_order(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.update_price()
#         instance.save()
#
#
# post_save.connect(post_save_order, sender=Order)

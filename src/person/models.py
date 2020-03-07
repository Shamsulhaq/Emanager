import os
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Expartmanager.utils import unique_slug_generator
from django.db import models
from django.db.models.signals import pre_save

from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL

fs = FileSystemStorage(location='media')


# Create your models here.


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Author image with new name by function
def upload_person_image_path(inistance, file_name):
    person_name = slugify(inistance.name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"person/{person_name}/{final_filename}"


class ExpertsQuerySet(models.query.QuerySet):
    def verify(self):  # for check is Activ
        return self.filter(is_verify=True)


class ExpertsManager(models.Manager):
    def get_queryset(self):
        return ExpertsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().verify()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            instance = qs.first()
        return instance


class Expert(models.Model):
    expert = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(upload_to=upload_person_image_path, blank=True)
    designation = models.CharField(max_length=255)
    Objective = models.TextField(blank=True, null=True)
    is_verify = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=False, auto_now=True)
    objects = ExpertsManager()

    def __str__(self):
        return self.expert.full_name

    class Meta:
        ordering = ['-last_update']

    @property
    def name(self):
        return self.expert.full_name

    def title(self):
        return self.name

    def phone(self):
        return self.expert.phone

    def email(self):
        return self.expert.email

    def nid(self):
        return self.expert.nid


def ba_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.is_verify:
        instance.is_online = True
    else:
        instance.is_online = False
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(ba_pre_save_receiver, sender=Expert)

# SKILL MODEL

LEVEL_CHOICES = (
    ('beginner', 'Beginner'),
    ('average', 'Average'),
    ('skilled', 'Skilled'),
    ('specialist', 'Specialist'),
    ('expert', 'Expert')
)


class Skill(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    training_institute = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=120, default='average', choices=LEVEL_CHOICES)
    is_verify = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['-timestamp']

    @property
    def name(self):
        return self.expert.name

    def phone(self):
        return self.expert.phone()

    def email(self):
        return self.expert.email()


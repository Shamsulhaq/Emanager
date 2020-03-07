from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db import models
from person.models import Expert


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone=None, email=None, nid=None, full_name=None, password=None, is_active=True,
                    is_staff=False,
                    is_admin=False):
        if not phone:
            raise ValueError("Users must have an phone number")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone=phone,
            nid=nid
        )
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, email=None, nid=None, full_name=None, password=None):
        user = self.create_user(
            phone,
            email=email,
            nid=nid,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, phone, email=None, nid=None, full_name=None, password=None):
        user = self.create_user(
            phone,
            email=email,
            nid=nid,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=17,
                             unique=True)  # validators should be a list
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    nid = models.CharField(max_length=17, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'phone'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['full_name']  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.full_name

    def get_short_name(self):
        if self.full_name:
            name = self.full_name
            name_obj = name.split(' ')
            sort_name = name_obj[0]
            return sort_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def is_verify(self):
        if self.nid:
            return True
        else:
            return False

    # @property
    # def is_active(self):
    #     return self.active


# class GuestEmail(models.Model):
#     email = models.EmailField()
#     active = models.BooleanField(default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.email
def expert_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.expert:
        user = User.objects.get(phone=instance.expert.phone)
        print(user)


post_save.connect(expert_created_receiver, sender=Expert)

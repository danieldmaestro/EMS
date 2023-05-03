from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.models import User
# from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
User = get_user_model()

class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    admin_fname = models.CharField(max_length=25)
    admin_lname = models.CharField(max_length=25)
    admin_email = models.EmailField()
    admin_phone_number = models.CharField(max_length=11)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=255)
    slug = models.SlugField()
    organisation = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name="departments")

    def __str__(self) -> str:
        return self.name


class JobTitle(models.Model):
    role = models.CharField(max_length=25)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.role
    

class Query(models.Model):
    employee = models.ForeignKey('Staff', on_delete=models.CASCADE)
    query_requester = models.ForeignKey('Staff', on_delete=models.CASCADE)
    reason = models.TextField()
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.employee} - {self.reason}'


@receiver(pre_save, sender=Organization)
def slugify_name(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)
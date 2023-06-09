from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class NigerianPhoneNumberField(PhoneNumberField):
    default_validators = [
        RegexValidator(
            r"^(?:\+?234|0)[789]\d{9}$",
            message="Please enter a valid Nigerian phone number starting with +234.",
            code="invalid_phone_number",
        ),
    ]

    def formfield(self, **kwargs):
        defaults = {
            "validators": self.default_validators,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    admin_fname = models.CharField(max_length=25)
    admin_lname = models.CharField(max_length=25)
    admin_email = models.EmailField()
    admin_username = models.CharField(max_length=25, unique=True)
    admin_phone_number = NigerianPhoneNumberField()
    company_email_domain = models.CharField(max_length=30, null=True)
    admin = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='organization', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("organization:org_detail", kwargs={"pk": self.pk, "org_slug": self.slug})

    def __str__(self) -> str:
        return self.name
    

class Department(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, related_name="departments", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("organization:dept_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name


class JobTitle(models.Model):
    role = models.CharField(max_length=25, unique=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, related_name="job_titles", blank=True, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, related_name="job_titles", blank=True, null=True)


    def get_absolute_url(self):
        return reverse("organization:job_title_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.role
    

def validate_csv_file(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('File must be a CSV file')   

class CsvFile(models.Model):
    file = models.FileField(upload_to='csv_files/', validators=[FileExtensionValidator(['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_save, sender=Organization)
def slugify_name(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Department)
def slugify_name(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

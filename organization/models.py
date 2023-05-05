from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
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
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    admin_fname = models.CharField(max_length=25)
    admin_lname = models.CharField(max_length=25)
    admin_email = models.EmailField()
    admin_username = models.CharField(max_length=50, unique=True)
    admin_phone_number = NigerianPhoneNumberField()
    company_email_domain = models.CharField(max_length=20, null=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization', blank=True, null=True)
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
    description = models.TextField(max_length=255, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name="jobtitles")

    def __str__(self) -> str:
        return self.role
    

class Query(models.Model):
    employee = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name="queries")
    query_requester = models.ForeignKey('Staff', on_delete=models.CASCADE)
    reason = models.TextField()
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.employee} - {self.reason}'
    

class Staff(models.Model):

    STATE_CHOICES = [(state, state) for state in (
        'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 
        'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT',
        'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 
        'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 
        'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'
    )]

    STAFF_STATUS = (
        ("Active", "Active"),
        ("On Leave", "On Leave"),
        ("Suspended", "Suspended"),
        ("Exited", "Exited"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='project_media/', null=True, blank=True)
    personal_email = models.EmailField()
    work_email = models.EmailField(blank=True)
    username = models.CharField(max_length=25, unique=True)
    phone_number = NigerianPhoneNumberField()
    date_of_birth = models.DateField()
    state_of_origin = models.CharField(max_length=25, choices=STATE_CHOICES)
    staff_status = models.CharField(max_length=10, choices=STAFF_STATUS, default="Active")
    salary = models.IntegerField()
    next_of_kin_name = models.CharField(max_length=50)
    next_of_kin_email = models.EmailField()
    next_of_kin_phone_number = NigerianPhoneNumberField()
    dept = models.OneToOneField(Department, on_delete=models.CASCADE,  blank=True)
    job_title = models.OneToOneField(JobTitle, on_delete=models.CASCADE, blank=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, blank=True)
    date_employed = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("staff_detail", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"



def validate_csv_file(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('File must be a CSV file')
    

class CsvFile(models.Model):
    file = models.FileField(upload_to='csv_files/', validators=[validate_csv_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Organization)
def slugify_name(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

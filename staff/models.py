from accounts.models import User
from django.db import models
from django.urls import reverse
from organization.models import Department, JobTitle, NigerianPhoneNumberField, Organization


# Create your models here.
class Query(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.SET_NULL, related_name="queries", null=True)
    query_requester = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    response = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name="queries", blank=True, null=True)
    is_responded = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.staff} - {self.reason}'
    

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

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="staff", null=True, blank=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    personal_email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER)
    work_email = models.EmailField(blank=True, null=True, unique=True)
    username = models.CharField(max_length=25, unique=True)
    phone_number = NigerianPhoneNumberField()
    date_of_birth = models.DateField()
    state_of_origin = models.CharField(max_length=25, choices=STATE_CHOICES)
    staff_status = models.CharField(max_length=10, choices=STAFF_STATUS, default="Active")
    next_of_kin_name = models.CharField(max_length=50)
    next_of_kin_email = models.EmailField()
    next_of_kin_phone_number = NigerianPhoneNumberField()
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name="staffs",  blank=True, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, related_name="staffs", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name="staffs", blank=True, null=True)
    date_employed = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("organization:staff_detail", kwargs={"pk": self.pk, "org_slug": self.organization.slug })

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    

class UserProfile(models.Model):
    staff_profile = models.OneToOneField(Staff, on_delete=models.SET_NULL, related_name="userprofile", null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.staff.first_name
    



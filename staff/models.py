from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# from django.contrib.auth.models import AbstractUser


User = get_user_model()
# Create your models here.

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='project_media/', null=True)
    personal_email = models.EmailField()
    work_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=11)
    d_o_b = models.DateField()
    state_of_origin = models.CharField(max_length=25, choices=STATE_CHOICES)
    next_of_kin = models.TextField(max_length=255)
    staff_status = models.CharField(max_length=10, choices=STAFF_STATUS)
    salary = models.IntegerField()
    dept = models.ForeignKey('Department', on_delete=models.CASCADE)
    job_title = models.ForeignKey('JobTitle', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    date_employed = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("staff_detail", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
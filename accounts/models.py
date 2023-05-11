from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class MyUserManager(UserManager):
    
    def create_org_admin(self, username, email, password, **extra_fields):
        """creates admin user"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        return self.create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    """Custom user model """
    email = models.EmailField(verbose_name = "email address", max_length=255, unique=True)
    
    objects = MyUserManager()
    
        


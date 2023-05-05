import random
import string

from django import forms
from django.utils.text import slugify

from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CsvFile, Department, JobTitle, Organization, Query, Staff



class DepartmentCreateForm(forms.ModelForm):
    """Form to create Department"""
    class Meta:
        model = Department
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['organization'].initial = user.organization
        self.fields['slug'].initial = slugify(self.cleaned_data['name'])


class JobTitleCreateForm(forms.ModelForm):
    """Form to Create Job Title"""
    class Meta:
        model = JobTitle
        fields = ["role", "department"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = user.departments.all()


class QueryCreateForm(forms.ModelForm):
    """Form to create query"""
    class Meta:
        model = Query
        fields = ['employee', 'query_requester', 'reason']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Filter staff queryset based on user's organization
        if user is not None:
            organization = user.organization
            self.fields['employee'].queryset = Staff.objects.filter(
                organization=organization)
            self.fields['query_requester'].queryset = Staff.objects.filter(
                organization=organization)


class QueryResponseForm(forms.ModelForm):
    """Form for query response"""
    class Meta:
        model = Query
        fields = ['response']


def generate_password(n=8):
    """Generate a random password of length n"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for _ in range(n))
    return password

class StaffCreateForm(forms.Form):
    class Meta:
        model = Staff
        fields = (
            'first_name', 'last_name', 'profile_picture', 'personal_email', 'username',
            'phone_number', 'date_of_birth', 'state_of_origin', 'next_of_kin', 'staff_status', 
            'salary', 'dept', 'job_title', 'organization',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['dept'].queryset = user.organization.departments.all()
        self.fields['job_title'].queryset = user.organization.jobtitles.all()
    
    def save(self, commit=True, *args, **kwargs):
        current_user = kwargs.pop("user", None)
        password = generate_password()
        staff = super().save(commit=False)
        if commit:
            staff.save()
        if not staff.user_id:
            user = User.objects.create_user(username=self.cleaned_data["username"],
                                            email=self.cleaned_data["work_email"],
                                            password=password)
            staff.user = user
            staff.work_email = f"{staff.first_name[0]}{staff.last_name}@{current_user.organization.company_email_domain}"
            staff.save()
        return staff


class OrganizationSignUpForm(forms.ModelForm):
    """Organization Signup Form"""
    name = forms.CharField(
        label='Organization Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'name',
                'placeholder': 'Organization Name'
            }
        )
    )
    company_email_domain = forms.CharField(
        label='Company Email Domain Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'company_email_domain',
                'placeholder': 'Company Email Domain'
            }
        )
    )
    address = forms.CharField(
        label='Organization Address',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'address',
                'placeholder': 'Organization Address'
            }
        )
    )
    admin_fname = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'admin_fname',
                'placeholder': 'Admin First Name'
            }
        )
    )
    admin_lname = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'admin_lname',
                'placeholder': 'Admin Last Name'
            }
        )
    )
    admin_username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'admin_username',
                'placeholder': 'Admin Username'
            }
        )
    )
    admin_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'admin_email',
                'placeholder': 'Admin Email'
            }
        )
    )
    admin_phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'admin_phone_number',
                'placeholder': 'Admin Phone Number'
            }
        ),
        error_messages={
            'invalid': 'Invalid phone number'
        }
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'password1',
                'placeholder': 'Enter Password'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg',
                'id': 'password2',
                'placeholder': 'Confirm Password'
            }
        )
    )
    class Meta:
        model = Organization
        fields = ["name", "address", "admin_fname", "company_email_domain",
                  "admin_lname", "admin_email", "admin_username", "admin_phone_number"]

    def clean_password2(self):
        print("lololol")
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2
    


class CsvFileForm(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.csv'})
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
        return file
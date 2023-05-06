
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

from .models import CsvFile, Department, JobTitle, Organization
from staff.models import Query, Staff


class DepartmentCreateForm(forms.ModelForm):
    """Form to create Department"""
    
    name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
    )
    description = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Department Description'}),
    )

    class Meta:
        model = Department
        fields = ('name', 'description', 'organization',)


class JobTitleCreateForm(forms.ModelForm):
    """Form to Create Job Title"""
    role = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Role'}),
    )
    department=forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'}),
    )

    class Meta:
        model = JobTitle
        fields = ("role", "department", 'description', "organization")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = user.organization.departments.all()


class QueryCreateForm(forms.ModelForm):
    """Form to create query"""
    staff = forms.ModelChoiceField(
        label='Query Recipient',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    query_requester = forms.ModelChoiceField(
        label='Query Requester',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    reason = forms.CharField(
        label='Reason for Query',
        max_length=60,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Next of Kin Fullname'}),
    )
    class Meta:
        model = Query
        fields = ('staff', 'query_requester', 'reason')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Filter staff queryset based on user's organization
        if user is not None:
            queryset =  user.organization.staffs.all()
            self.fields['staff'].queryset = queryset
            self.fields['query_requester'].queryset = queryset

    def clean(self):
        cleaned_data = super().clean()
        staff = cleaned_data.get('staff')
        query_requester = cleaned_data.get('query_requester')
        if staff == query_requester:
            raise forms.ValidationError("Staff and Query Requester cannot be the same.")
        return cleaned_data


class QueryResponseForm(forms.ModelForm):
    """Form for query response"""
    class Meta:
        model = Query
        fields = ['response']


class StaffCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=Staff.GENDER,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
    )
    personal_email = forms.EmailField(
        label='Personal Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Personal Email'}),
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
    )
    state_of_origin = forms.ChoiceField(
        label='State of Origin',
        choices=Staff.STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'State of Origin'}),
    )
    next_of_kin_name = forms.CharField(
        label='Next of Kin Fullname',
        max_length=60,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Next of Kin Fullname'}),
    )
    next_of_kin_email = forms.EmailField(
        label='Next of Kin Email',
        max_length=60,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Next of Kin Email'}),
    )
    next_of_kin_phone_number = forms.CharField(
        label='Next of Kin Phone Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Next of Kin Phone Number'}),
    )
    staff_status = forms.ChoiceField(
        label='Staff Status',
        choices=Staff.STAFF_STATUS,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dept = forms.ModelChoiceField(
        label='Department',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    job_title = forms.ModelChoiceField(
        label='Job Title',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    # organization = forms.ModelChoiceField(
    #     label='Organization',
    #     queryset=None,
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    # )
    class Meta:
        model = Staff
        fields = (
            'first_name', 'last_name', 'gender', 'personal_email', 'username',
            'phone_number', 'date_of_birth', 'state_of_origin', 'next_of_kin_name', 'next_of_kin_email',
            'next_of_kin_phone_number', 'staff_status', 'dept', 'job_title', 'organization',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.fields['dept'].queryset = user.organization.departments.all()
        self.fields['job_title'].queryset = user.organization.job_titles.all()



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
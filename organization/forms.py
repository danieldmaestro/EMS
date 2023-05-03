from django import forms
from .models import Organization, Department, JobTitle, Query
from django.utils.text import slugify
from accounts.models import User
from staff.models import Staff


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


class OrganizationSignUpForm(forms.ModelForm):
    """Organization Signup Form"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = Organization
        fields = ["name", "address", "admin_fname",
                  "admin_lname", "admin_email", "admin_phone_number"]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        organization = super().save(commit=False)
        if commit:
            organization.save()
        if not organization.admin_id:
            # If the organization is being created for the first time,
            # create a new User instance and assign it to the admin field
            admin = User.objects.create_org_admin(
                email=self.cleaned_data["admin_email"],
                password=self.cleaned_data['password1'],
            )
            organization.admin = admin
            organization.save()
        return organization

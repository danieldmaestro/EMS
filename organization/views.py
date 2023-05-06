import random
import string

from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Organization, Department, JobTitle
from staff.models import Staff, Query
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import StaffCreateForm, QueryResponseForm, DepartmentCreateForm, JobTitleCreateForm, OrganizationSignUpForm


class AdminDashboardView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Staff
    template_name = 'organization/dashboard.html'
    context_object_name = 'staff_list'

    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.organization)
    
def generate_password(n=8):
    """Generate a random password of length n"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for _ in range(n))
    return password

class OrgDetailView(DetailView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Organization
    template_name = "organization/org_detail.html"
    context_object_name = "org"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(admin=user)
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)


class OrgUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Organization
    success_url = reverse_lazy("organization:admin_dashboard")
    template_name = "organization/org_form.html"
    fields = ("name", "address", "admin_fname", "company_email_domain",
                  "admin_lname", "admin_email", "admin_username", "admin_phone_number")

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.save()
        return super().form_valid(form)



class StaffCreateView(CreateView, LoginRequiredMixin,PermissionRequiredMixin):
    form_class = StaffCreateForm
    success_url = reverse_lazy("organization:admin_dashboard")
    template_name = "organization/staff_create_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        current_user = self.request.user
        staff = form.save(commit=False)
        staff.work_email = f"{staff.first_name[0].lower()}{staff.last_name.lower()}@{current_user.organization.company_email_domain}"
        staff.organization = current_user.organization
        password = generate_password()
        # create a new user and assign it to the admin field
        user = User.objects.create_user(username=staff.username,
                                        email=staff.work_email,
                                        password=password,
        )
        staff.user = user
        staff.save()
        return super().form_valid(form)
    
class StaffDetailView(DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Staff
    template_name = "organization/staff_detail.html"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(organization=user.organization)
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)

class StaffUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Staff
    template_name = "organization/staff_update_form.html"
    fields = (
            'first_name', 'last_name', 'gender', 'personal_email',
            'phone_number', 'date_of_birth', 'state_of_origin', 'next_of_kin_name', 'next_of_kin_email',
            'next_of_kin_phone_number', 'staff_status', 'dept', 'job_title',
        )

    
    def form_valid(self, form):
        staff = form.save(commit=False)
        staff.save()
        return super().form_valid(form)
    

class DepartmentListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Staff
    template_name = 'organization/department_list.html'
    context_object_name = 'dept_list'

    def get_queryset(self):
        oraganization = self.request.user.organization
        return oraganization.departments.all()
    

class DepartmentCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = DepartmentCreateForm
    success_url = reverse_lazy("organization:department_list")
    template_name = "organization/department_form.html"

    
    def form_valid(self, form):
        dept = form.save(commit=False)
        dept.organization = self.request.user.organization
        dept.save()
        return super().form_valid(form)
    

class DepartmentUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Department
    template_name = "organization/department_form.html"
    success_url = reverse_lazy("organization:department_list")
    fields = ('name', 'description', )

    
    def form_valid(self, form):
        dept = form.save(commit=False)
        dept.save()
        return super().form_valid(form)
    
class JobTitleListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = JobTitle
    template_name = 'organization/job_title_list.html'
    context_object_name = 'job_title_list'

    def get_queryset(self):
        oraganization = self.request.user.organization
        return oraganization.job_titles.all()
    

class JobTitleCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = JobTitleCreateForm
    success_url = reverse_lazy("organization:job_title_list")
    template_name = "organization/job_title_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        job_title = form.save(commit=False)
        job_title.organization = self.request.user.organization
        job_title.save()
        return super().form_valid(form)
    

class JobtTitleUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = JobTitle
    template_name = "organization/job_title_form.html"
    success_url = reverse_lazy("organization:job_title_list")
    fields = ('role', 'description', )

    
    def form_valid(self, form):
        job_title = form.save(commit=False)
        job_title.save()
        return super().form_valid(form)
    
    
    






# class OrganizationUpdateView(UpdateView):
#     model = Organization
#     form_class = OrganizationForm
#     template_name = 'employee/organization_form.html'


# class DepartmentCreateView(CreateView):
#     model = Department
#     form_class = DepartmentForm
#     template_name = 'employee/department_form.html'


# class DepartmentUpdateView(UpdateView):
#     model = Department
#     form_class = DepartmentForm
#     template_name = 'employee/department_form.html'


# class JobTitleCreateView(CreateView):
#     model = JobTitle
#     form_class = JobTitleForm
#     template_name = 'employee/jobtitle_form.html'


# class JobTitleUpdateView(UpdateView):
#     model = JobTitle
#     form_class = JobTitleForm
#     template_name = 'employee/jobtitle_form.html'


# class EmployeeCreateView(CreateView):
#     model = Staff
#     form_class = EmployeeForm
#     template_name = 'employee/employee_form.html'


# class EmployeeUpdateView(UpdateView):
#     model = Staff
#     form_class = EmployeeForm
#     template_name = 'employee/employee_form.html'


# class QueryCreateView(CreateView):
#     model = Query
#     form_class = QueryForm
#     template_name = 'employee/query_form.html'

#     def get_initial(self):
#         initial = super().get_initial()
#         employee_id = self.kwargs.get('pk')
#         employee = get_object_or_404(Staff, id=employee_id)
#         initial['employee'] = employee
#         return initial


# class QueryResponseUpdateView(UpdateView):
#     model = Query
#     form_class = QueryResponseForm
#     template_name = 'employee/queryresponse_form.html'



# class EmployeeDetailView(DetailView):
#     model = Staff
#     template_name = 'employee/employee_detail.html'
#     context_object_name = 'employee'


# class UserProfileUpdateView(UpdateView):
#     model = UserProfile
#     form_class = UserProfileForm
#     template_name = 'employee/userprofile_form.html'
#     success_url = reverse_lazy('employee:dashboard')

#     def get_object(self):
#         return self.request.user.userprofile
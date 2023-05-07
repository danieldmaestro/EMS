import csv
import random
import string

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, View
from django.urls import reverse_lazy, reverse
from .models import Organization, Department, JobTitle
from staff.models import Staff, Query
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import StaffCreateForm, DepartmentCreateForm, JobTitleCreateForm, QueryCreateForm, CsvFileForm


class AdminDashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'organization/dashboard.html'
    context_object_name = 'staff_list'
    raise_exception = True

    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.organization)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug


class OrgDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Organization
    template_name = "organization/org_detail.html"
    context_object_name = "org"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(admin=user)
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug


class OrgUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Organization
    success_url = reverse_lazy("organization:admin_dashboard")
    template_name = "organization/org_form.html"
    fields = ("name", "address", "admin_fname", "company_email_domain",
                  "admin_lname", "admin_email", "admin_username", "admin_phone_number")

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.save()
        return super().form_valid(form)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug


def generate_password(n=8):
    """Generate a random password of length n"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for _ in range(n))
    return password


class StaffCreateChoiceView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = "organization/staff_create.html"

    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug



class StaffCreateFormView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
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
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    
class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Staff
    template_name = "organization/staff_detail.html"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(organization=user.organization)
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'organization/department_list.html'
    context_object_name = 'dept_list'

    def get_queryset(self):
        oraganization = self.request.user.organization
        return oraganization.departments.all()
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = DepartmentCreateForm
    success_url = reverse_lazy("organization:department_list")
    template_name = "organization/department_form.html"

    
    def form_valid(self, form):
        dept = form.save(commit=False)
        dept.organization = self.request.user.organization
        dept.save()
        return super().form_valid(form)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Department
    template_name = "organization/department_form.html"
    success_url = reverse_lazy("organization:department_list")
    fields = ('name', 'description', )

    
    def form_valid(self, form):
        dept = form.save(commit=False)
        dept.save()
        return super().form_valid(form)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    
class JobTitleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = JobTitle
    template_name = 'organization/job_title_list.html'
    context_object_name = 'job_title_list'

    def get_queryset(self):
        oraganization = self.request.user.organization
        return oraganization.job_titles.all()
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class JobTitleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
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
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    

class JobtTitleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = JobTitle
    template_name = "organization/job_title_form.html"
    success_url = reverse_lazy("organization:job_title_list")
    fields = ('role', 'description', )

    
    def form_valid(self, form):
        job_title = form.save(commit=False)
        job_title.save()
        return super().form_valid(form)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    
    
class QueryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = QueryCreateForm
    success_url = reverse_lazy("organization:query_list")
    template_name = "organization/query_form.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        query = form.save(commit=False)
        query.organization = self.request.user.organization
        query.save()
        return super().form_valid(form)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug

class QueryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Query
    template_name = 'organization/query_list.html'
    context_object_name = 'query_list'

    def get_queryset(self):
        return self.request.user.organization.queries.all()
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
    
class QueryResponseView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Query
    template_name = "organization/query_response.html"

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset.filter(organization=user.organization)
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug


class CreateStaffFromCSV(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'organization/staff_create_from_csv.html'
    
    def get(self, request, *args, **kwargs):
        form = CsvFileForm
        context = {'form': form }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        current_org = request.user.organization
        slug = current_org.slug

        if not csv_file:
            messages.error(request, 'Please select a CSV file.')
            return HttpResponseRedirect(reverse("organization:staff_create_csv", kwargs={'org_slug': slug }))

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            with transaction.atomic():
                for row in reader:
                    staff = Staff(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        personal_email=row['personal_email'],
                        gender=row['gender'],
                        username=row['username'],
                        phone_number=row['phone_number'],
                        date_of_birth=row['date_of_birth'],
                        state_of_origin=row['state_of_origin'],
                        staff_status=row['staff_status'],
                        next_of_kin_name=row['next_of_kin_name'],
                        next_of_kin_email=row['next_of_kin_email'],
                        next_of_kin_phone_number=row['next_of_kin_phone_number'],
                        dept_id=row['dept_id'],
                        job_title_id=row['job_title_id'],   
                    )
                    try:
                        staff.full_clean()
                    except ValidationError as e:
                        messages.error(request, f"Error on row {reader.line_num}: {e}")
                        return HttpResponseRedirect(reverse("organization:staff_create_csv", kwargs={'org_slug': slug }))
                    try:
                        staff.work_email = f"{staff.first_name[0].lower()}{staff.last_name.lower()}@{current_org.company_email_domain}"
                        staff.organization = current_org
                        password = generate_password()
                        user = User.objects.create_user(username=staff.username,
                                    email=staff.work_email,
                                    password=password,
                                    )
                        staff.user = user
                        staff.save()
                    except IntegrityError:
                        transaction.rollback()
                        messages.error(request, f"Error on row {reader.line_num}: Staff with username '{row['username']}' already exists.")
                        return HttpResponseRedirect(reverse("organization:staff_create_csv", kwargs={'org_slug': slug }))
        except csv.Error as e:
            messages.error(request, f'Error processing CSV file: {e}')
            return HttpResponseRedirect(reverse("organization:staff_create_csv", kwargs={'org_slug': slug }))
            

        messages.success(request, 'Staff successfully created.')
        return HttpResponseRedirect(reverse("organization:admin_dashboard",  kwargs={'org_slug': slug }))

    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.organization.slug == org_slug
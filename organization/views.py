from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Organization, Department, JobTitle, Employee, Query, UserProfile
from .forms import OrganizationForm, DepartmentForm, JobTitleForm, EmployeeForm, QueryForm, QueryResponseForm, UserProfileForm


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'employee/organization_form.html'


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'employee/organization_form.html'


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employee/department_form.html'


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employee/department_form.html'


class JobTitleCreateView(CreateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'employee/jobtitle_form.html'


class JobTitleUpdateView(UpdateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = 'employee/jobtitle_form.html'


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'


class QueryCreateView(CreateView):
    model = Query
    form_class = QueryForm
    template_name = 'employee/query_form.html'

    def get_initial(self):
        initial = super().get_initial()
        employee_id = self.kwargs.get('pk')
        employee = get_object_or_404(Employee, id=employee_id)
        initial['employee'] = employee
        return initial


class QueryResponseUpdateView(UpdateView):
    model = Query
    form_class = QueryResponseForm
    template_name = 'employee/queryresponse_form.html'


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'employee/userprofile_form.html'
    success_url = reverse_lazy('employee:dashboard')

    def get_object(self):
        return self.request.user.userprofile
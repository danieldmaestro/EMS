from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import ProfilePictureForm, QueryResponseForm
from .models import Query, Staff, UserProfile

# Create your views here.
class StaffDashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Staff
    template_name = 'staff/dashboard.html'
    context_object_name = 'staff_list'
    raise_exception = True

    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.staff.organization)
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.staff.organization.slug == org_slug and not self.request.user.is_staff
    

class StaffProfileView(LoginRequiredMixin,PermissionRequiredMixin, TemplateView):
    model = UserProfile
    template_name = 'staff/staff_profile.html'

    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.staff.organization.slug == org_slug and not self.request.user.is_staff
    

class UploadProfilePictureView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'staff/upload_profile_picture.html'
    form_class = ProfilePictureForm

    def form_valid(self, form):
        profile_picture = form.cleaned_data['profile_picture']
        # profile_picture = self.request.FILES.get('profile_picture')
        self.request.user.staff.userprofile.profile_picture = profile_picture
        self.request.user.staff.userprofile.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            "staff:staff_profile",
            kwargs={"org_slug": self.request.user.staff.organization.slug}
        )
    
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.staff.organization.slug == org_slug and not self.request.user.is_staff
    

class StaffQueryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Query
    template_name = "staff/query_list.html"
    context_object_name = 'query_list'
    raise_exception = True

    def get_queryset(self):
        queryset = self.request.user.staff.queries.all()
        return queryset
        
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.staff.organization.slug == org_slug and not self.request.user.is_staff
    

class StaffQueryResponseView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Query
    form_class = QueryResponseForm
    template_name = "staff/query_form.html"

    def form_valid(self, form):
        query = form.save(commit=False)
        query.is_responded = True  # Set is_responded to True
        query.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            "staff:query_list",
            kwargs={"org_slug": self.request.user.staff.organization.slug}
        )
        
    def has_permission(self):
        org_slug = self.kwargs['org_slug']
        return self.request.user.staff.organization.slug == org_slug and not self.request.user.is_staff

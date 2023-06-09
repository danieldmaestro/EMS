from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from django.contrib.auth import views as auth_views

from organization.forms import OrganizationSignUpForm

# Create your views here.
class SignUp(CreateView):
    form_class = OrganizationSignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        organization = form.save(commit=False)
        # create a new user and assign it to the admin field
        admin = User.objects.create_org_admin(
            username=form.cleaned_data['admin_username'],
            email=form.cleaned_data["admin_email"],
            password=form.cleaned_data['password1'],
            first_name=form.cleaned_data["admin_fname"],
            last_name=form.cleaned_data["admin_lname"],
        )
        organization.admin = admin
        organization.save()
        return super().form_valid(form)
    
    
class CustomPasswordReset(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")

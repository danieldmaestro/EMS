from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User

from organization import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.OrganizationSignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        print('lololol')
        organization = form.save(commit=False)
        # create a new user and assign it to the admin field
        admin = User.objects.create_org_admin(
            username=form.cleaned_data['admin_username'],
            email=form.cleaned_data["admin_email"],
            password=form.cleaned_data['password1'],
        )
        organization.admin = admin
        organization.save()
        return super().form_valid(form)
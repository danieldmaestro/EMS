"""
URL configuration for EMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from organization.api.views import OrganizationCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", views.HomePage.as_view(), name='home'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/admin/", OrganizationCreateAPIView.as_view(), name="signup"),
    path("api/admin/<slug:org_slug>/", include("organization.api.urls", namespace="org_api")),
    path("api/staff/<slug:org_slug>/", include("staff.api.urls", namespace="staff_api")),
    path('ems/<slug:org_slug>/dashboard/admin/', include('organization.urls')),
    path('ems/<slug:org_slug>/dashboard/staff/', include('staff.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


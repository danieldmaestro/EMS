from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path("", views.StaffDashboardView.as_view(), name="staff_dashboard"),
    path("profile/", views.StaffProfileView.as_view(), name="staff_profile"),
    path("profile/upload_photo/", views.UploadProfilePictureView.as_view(), name="upload_photo"),
    path("queries/", views.StaffQueryListView.as_view(), name="query_list"),
    path("queries/<int:pk>/respond", views.StaffQueryResponseView.as_view(), name="query_response"),

]

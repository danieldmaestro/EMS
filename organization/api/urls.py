from django.urls import path
from . import views

app_name = "org_api"
urlpatterns = [
    path("", views.OrganizationDetailAPIView.as_view(), name="organization-detail"),
    path("update/", views.OrganizationUpdateAPIView.as_view(), name="organization-update"),
    path("departments/", views.DepartmentListCreateAPIView.as_view(), name="dept_list_create"),
    path("departments/<int:pk>/", views.DepartmentDetailUpdateAPIView.as_view(), name="department-detail"),
    path("jobtitles/", views.JobTitleListCreateAPIView.as_view(), name="job_title_list_create"),
    path("jobtitles/<int:pk>/", views.JobTitleDetailUpdateDeleteAPIView.as_view(), name="job-title-detail"),
    path("staffs/", views.StaffListCreateAPIView.as_view(), name="staff_list_create"),
    path("staffs/csv/", views.StaffCreateFromCSVAPIView.as_view(), name="staff_create_from_csv"),
    path("staffs/<int:pk>/", views.StaffDetailUpdateAPIView.as_view(), name="staff-detail"),
    path("queries/", views.QueryListCreateAPIView.as_view(), name="query_list_create"),
    path("queries/<int:pk>/", views.QueryViewResponseAPIView.as_view(), name="query-detail"),
]


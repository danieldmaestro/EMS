from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/admin/<int:pk>', views.OrgDetailView.as_view(), name='org_detail'),
    path('dashboard/admin/<int:pk>/update', views.OrgUpdateView.as_view(), name='org_update'),
    path('dashboard/admin/staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('dashboard/admin/staff/<int:pk>/', views.StaffDetailView.as_view(), name="staff_detail"),
    path('dashboard/admin/staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name="staff_update"),
    path('dashboard/admin/departments/', views.DepartmentListView.as_view(), name="department_list"),
    path('dashboard/admin/departments/create', views.DepartmentCreateView.as_view(), name="dept_create"),
    path('dashboard/admin/departments/<int:pk>/update', views.DepartmentUpdateView.as_view(), name="dept_update"),
    path('dashboard/admin/jobtitles/', views.JobTitleListView.as_view(), name="job_title_list"),
    path('dashboard/admin/jobtitles/create', views.JobTitleCreateView.as_view(), name="job_title_create"),
    path('dashboard/admin/jobtitles/<int:pk>/update', views.JobtTitleUpdateView.as_view(), name="job_title_update"),
]

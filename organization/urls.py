from django.urls import path, include
from . import views

app_name = 'organization'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('<int:pk>/', views.OrgDetailView.as_view(), name='org_detail'),
    path('<int:pk>/update/', views.OrgUpdateView.as_view(), name='org_update'),
    path('staff/create/', views.StaffCreateChoiceView.as_view(), name='staff_create'),
    path('staff/create/csv/', views.CreateStaffFromCSV.as_view(), name='staff_create_csv'),
    path('staff/create/form/', views.StaffCreateFormView.as_view(), name='staff_create_form'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name="staff_detail"),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name="staff_update"),
    path('departments/', views.DepartmentListView.as_view(), name="department_list"),
    path('departments/create/', views.DepartmentCreateView.as_view(), name="dept_create"),
    path('departments/<int:pk>/update', views.DepartmentUpdateView.as_view(), name="dept_update"),
    path('jobtitles/', views.JobTitleListView.as_view(), name="job_title_list"),
    path('jobtitles/create/', views.JobTitleCreateView.as_view(), name="job_title_create"),
    path('jobtitles/<int:pk>/update/', views.JobtTitleUpdateView.as_view(), name="job_title_update"),
    path('queries/', views.QueryListView.as_view(), name="query_list"),
    path('queries/create/', views.QueryCreateView.as_view(), name="query_create"),
    path('queries/<int:pk>/response/', views.QueryResponseView.as_view(), name="query_response"),
]

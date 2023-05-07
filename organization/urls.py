from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('<slug:org_slug>/dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('<slug:org_slug>/dashboard/admin/<int:pk>', views.OrgDetailView.as_view(), name='org_detail'),
    path('<slug:org_slug>/dashboard/admin/<int:pk>/update', views.OrgUpdateView.as_view(), name='org_update'),
    path('<slug:org_slug>/dashboard/admin/staff/create/', views.StaffCreateChoiceView.as_view(), name='staff_create'),
    path('<slug:org_slug>/dashboard/admin/staff/create/csv', views.CreateStaffFromCSV.as_view(), name='staff_create_csv'),
    path('<slug:org_slug>/dashboard/admin/staff/create/form', views.StaffCreateFormView.as_view(), name='staff_create_form'),
    path('<slug:org_slug>/dashboard/admin/staff/<int:pk>/', views.StaffDetailView.as_view(), name="staff_detail"),
    path('<slug:org_slug>/dashboard/admin/staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name="staff_update"),
    path('<slug:org_slug>/dashboard/admin/departments/', views.DepartmentListView.as_view(), name="department_list"),
    path('<slug:org_slug>/dashboard/admin/departments/create', views.DepartmentCreateView.as_view(), name="dept_create"),
    path('<slug:org_slug>/dashboard/admin/departments/<int:pk>/update', views.DepartmentUpdateView.as_view(), name="dept_update"),
    path('<slug:org_slug>/dashboard/admin/jobtitles/', views.JobTitleListView.as_view(), name="job_title_list"),
    path('<slug:org_slug>/dashboard/admin/jobtitles/create', views.JobTitleCreateView.as_view(), name="job_title_create"),
    path('<slug:org_slug>/dashboard/admin/jobtitles/<int:pk>/update', views.JobtTitleUpdateView.as_view(), name="job_title_update"),
    path('<slug:org_slug>/dashboard/admin/queries', views.QueryListView.as_view(), name="query_list"),
    path('<slug:org_slug>/dashboard/admin/queries/create', views.QueryCreateView.as_view(), name="query_create"),
    path('<slug:org_slug>/dashboard/admin/queries/<int:pk>/response', views.QueryResponseView.as_view(), name="query_response"),
]

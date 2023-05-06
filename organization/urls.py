from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('dashboard/admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/admin/staff/create/', views.StaffCreateView.as_view(), name='staff_create_form'),
    path('dashboard/admin/staff/<int:pk>/', views.StaffDetailView.as_view(), name="staff_detail"),
    path('dashboard/admin/staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name="staff_update"),
    path('dashboard/admin/departments/', views.DepartmentListView.as_view(), name="department_list"),
    path('dashboard/admin/departments/create', views.DepartmentCreateView.as_view(), name="dept_create"),
    path('dashboard/admin/departments/<int:pk>/update', views.DepartmentUpdateView.as_view(), name="dept_update"),
]

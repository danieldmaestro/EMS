from django.urls import path
from . import views

app_name = "staff_api"

urlpatterns = [
    path("staffs/", views.StaffListView.as_view(), name="staff_list"),
    path("queries/", views.CurrentStaffQueriesListAPIView.as_view(), name="query_list"),
    path("queries/<int:pk>/", views.QueryUpdateResponse.as_view(), name="query_response"),
    path("profile/", views.StaffUserProfileDetailAPIView.as_view(), name="staff_profile"),
    path("profile/upload/", views.StaffPictureUploadAPIView.as_view(), name="picture_upload"),
]

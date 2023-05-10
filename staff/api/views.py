from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import StaffSerializer, QuerySerializer, UserProfileSerializer
from ..models import Staff, Query, UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from organization.api.permissions import IsPartOfOrg


class StaffListView(generics.ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg]

    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.organization)
    

class StaffUserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg]
    
    def get_object(self):
        return self.user.staff.userprofile
    

class StaffPictureUploadAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg]
    parser_class = (FileUploadParser,)

    def get_object(self):
        return self.user.staff.userprofile

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'profile_picture' not in request.data:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.data['profile_picture']
        instance.profile_picture.save(file.name, file, save=True)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class CurrentStaffQueriesListAPIView(generics.ListAPIView):
    serializer_class = QuerySerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg]

    def get_queryset(self):
        return self.request.user.staff.queries.all()
    

class QueryUpdateResponse(generics.UpdateAPIView):
    serializer_class = QuerySerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.response = request.data.get('response', instance.response)
        instance.is_responded = True
        instance.save(update_fields=['response', 'is_responded'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.request.user.staff.queries.all()

    def get_serializer_class(self):
        return self.serializer_class
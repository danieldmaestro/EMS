import csv
import string
import random

from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import generics, status 
from rest_framework.response import Response 
from ..models import Department,Organization, JobTitle
from .serializers import OrganizationSerializer, DepartmentSerializer, JobTitleSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsPartOfOrg
from accounts.models import User
from staff.models import Staff, Query
from staff.api.serializers import StaffSerializer, QuerySerializer
from staff.models import UserProfile


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def perform_create(self, serializer):
        department = serializer.save(organization=self.request.user.organization)
        return department
    
    def get_queryset(self):
        return Department.objects.filter(organization=self.request.user.organization)
    

class DepartmentDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_queryset(self):
        return Department.objects.filter(organization=self.request.user.organization)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            'pk': self.kwargs['pk'],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class JobTitleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobTitleSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def perform_create(self, serializer):
        dept_name = serializer.validated_data.pop('dept_name')
        department = get_object_or_404(Department, name__iexact=dept_name)
        job_title = serializer.save(organization=self.request.user.organization, department=department)
        return job_title
    
    def get_queryset(self):
        return JobTitle.objects.filter(organization=self.request.user.organization)
    
    
class JobTitleDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobTitleSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_queryset(self):
        return JobTitle.objects.filter(organization=self.request.user.organization)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            'pk': self.kwargs['pk'],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer

    def perform_create(self, serializer):
        user = User.objects.create_org_admin(username=serializer.validated_data['admin_username'],
                                            email=serializer.validated_data['admin_email'],
                                            password=serializer.validated_data['password1'],
                                            first_name=serializer.validated_data['admin_fname'],
                                            last_name=serializer.validated_data['admin_lname'],
        )
        validated_data = serializer.validated_data.copy()
        validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        organization = serializer.Meta.model.objects.create(admin=user, **validated_data)
        serializer.instance = organization
        return organization


class OrganizationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_object(self):
        return self.request.user.organization
    
class OrganizationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_object(self):
        return self.request.user.organization


def generate_password(n=8):
    """Generate a random password of length n"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for _ in range(n))
    return password


class StaffListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def perform_create(self, serializer):
        current_org = self.request.user.organization
        staff = serializer.validated_data
        # Get Department Instance
        dept_name = staff.pop('dept_name')
        department = get_object_or_404(Department, name__iexact=dept_name)
        # Get Jobtitle instance
        job_title_role = staff.pop('job_title_role')
        job_title = get_object_or_404(JobTitle, role__iexact=job_title_role)
        # Generate work email
        work_email = f"{staff['first_name'][0].lower()}{staff['last_name'].lower()}@{current_org.company_email_domain}"
        # Generate password
        password = generate_password()
        print(f"Password for {staff['username']} is {password}")
        # Create Staff User and bind to Staff instance
        user = User.objects.create_user(username=staff['username'],
            email=work_email,
            password=password,
            first_name=staff['first_name'],
            last_name=staff['last_name'],
        )
        staff.user = user
        staff_instance = serializer.save(user=user, work_email=work_email, organization=current_org, dept=department, job_title=job_title)
        UserProfile.objects.create(staff_profile=staff_instance)
        return staff_instance
    
    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.organization)
    
    
class StaffDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_queryset(self):
        return Staff.objects.filter(organization=self.request.user.organization)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            'pk': self.kwargs['pk'],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class StaffCreateFromCSVAPIView(generics.CreateAPIView):
    serializer_class = StaffSerializer

    def post(self, request, *args, **kwargs):
        csv_file = request.data.get('file')
        current_org = request.user.organization
        if not csv_file:
             return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            with transaction.atomic():
                for row in reader:
                    try:
                        work_email = f"{row['first_name'][0].lower()}{row['last_name'].lower()}@{current_org.company_email_domain}"
                        password = generate_password()
                        print(f"{row['username']} : {password}")
                        user = User.objects.create_user(username=row['username'],
                                        email=work_email,
                                        password=password,
                                        first_name=row['first_name'],
                                        last_name=row['last_name'],
                                    )
                        serializer = self.get_serializer(data=row)
                        serializer.is_valid(raise_exception=True)
                        dept_name = serializer.validated_data.pop('dept_name')
                        department = get_object_or_404(Department, name__iexact=dept_name)
                        job_title_role = serializer.validated_data.pop('job_title_role')
                        job_title = get_object_or_404(JobTitle, role__iexact=job_title_role)
                        staff_instance = serializer.save(user=user, work_email=work_email, organization=current_org, dept=department, job_title=job_title)
                        UserProfile.objects.create(staff_profile=staff_instance)
                    except IntegrityError:
                        transaction.rollback()
                        return Response({{"Error": f"Error on row {reader.line_num}: Staff with username '{row['username']}' already exists."}})
        except csv.Error as e:
            return Response({"Error": f'Error processing CSV file: {e}'})
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            

class QueryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = QuerySerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]
    
    def perform_create(self, serializer):
        staff_fname = serializer.validated_data.pop('staff_fname')
        query_requester_fname = serializer.validated_data.pop('query_requester_fname')
        staff = get_object_or_404(Staff, first_name__iexact=staff_fname)
        query_requester = get_object_or_404(Staff, first_name__iexact=query_requester_fname)
        query = serializer.save(organization=self.request.user.organization, staff=staff, query_requester=query_requester)
        return query
    
    def get_queryset(self):
        return Query.objects.filter(organization=self.request.user.organization)
    
    
class QueryViewResponseAPIView(generics.RetrieveAPIView):
    serializer_class = QuerySerializer
    permission_classes = [IsAuthenticated, IsPartOfOrg, IsAdminUser]

    def get_queryset(self):
        return Query.objects.filter(organization=self.request.user.organization)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            'pk': self.kwargs['pk'],
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
    



    
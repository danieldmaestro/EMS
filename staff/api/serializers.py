from rest_framework import serializers
from rest_framework.reverse import reverse
from organization.models import Department, JobTitle
from staff.models import Query, Staff, UserProfile


class CustomHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """Custom HyperlinkedRelatedField for URLs with two lookup kwargs(org_slug and pk)"""
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'org_slug': request.user.organization.slug,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['org_slug'],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
    

class CustomHyperlinkedIdentityField(serializers.HyperlinkedIdentityField, CustomHyperlinkedRelatedField):
    """Custom HyperlinkedIdentityField for URLs with two lookup kwargs(org_slug and pk)"""

    pass


class OrgCustomHyperlinkedIdentityField(serializers.HyperlinkedRelatedField):
    """Custom HyperlinkedIdentityField for organization URLs with one lookup kwarg(org_slug)"""

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'org_slug': request.user.organization.slug,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['org_slug'],
        }
        return self.get_queryset().get(**lookup_kwargs)
    
    
class StaffCustomHyperlinkedIdentityField(serializers.HyperlinkedIdentityField, CustomHyperlinkedRelatedField):
    """Custom HyperlinkedIdentityField for staff URLs with one lookup kwarg(org_slug)"""

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'org_slug': request.user.staff.organization.slug,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['org_slug'],
        }
        return self.get_queryset().get(**lookup_kwargs)


class QuerySerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlinkedIdentityField(view_name="org_api:query-detail", read_only=True)
    organization = OrgCustomHyperlinkedIdentityField(view_name='org_api:organization-detail', read_only=True)
    staff = CustomHyperlinkedRelatedField(view_name='org_api:staff-detail', read_only=True)
    query_requester = CustomHyperlinkedRelatedField(view_name='org_api:staff-detail', read_only=True)
    staff_fname = serializers.CharField(write_only=True)
    query_requester_fname = serializers.CharField(write_only=True)
    
    class Meta:
        model = Query
        fields = ['url', 'id', 'staff', 'query_requester', 'reason', 'response',
                'organization', 'is_responded', 'staff_fname', 'query_requester_fname']


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlinkedIdentityField(view_name="org_api:staff-detail", read_only=True)
    dept = CustomHyperlinkedRelatedField(view_name='org_api:department-detail', read_only=True)
    organization = OrgCustomHyperlinkedIdentityField(view_name='org_api:organization-detail', read_only=True)
    job_title = CustomHyperlinkedRelatedField(view_name="org_api:job-title-detail", read_only=True)
    dept_name = serializers.CharField(write_only=True)
    job_title_role = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['url', 'id', 'first_name', 'last_name', 'personal_email', 'work_email', 'gender','username', 'phone_number',
                   'date_of_birth', 'state_of_origin', 'staff_status', 'next_of_kin_name', 'next_of_kin_email', 
                   'next_of_kin_phone_number', 'dept', 'dept_name', 'job_title', 'job_title_role', 'organization', 'date_employed']
    
    def validate(self, data):
        # get the department and job title from the data
        dept_name = data.get('dept_name')
        job_title_role = data.get('job_title_role')

        # check if the job title's department matches the given department
        try:
            department = Department.objects.get(name=dept_name, organization=self.context['request'].user.organization)
            job_title = JobTitle.objects.get(role=job_title_role, department=department)
        except (Department.DoesNotExist, JobTitle.DoesNotExist):
            raise serializers.ValidationError("Invalid department or job title.")

        if job_title.department != department:
            raise serializers.ValidationError("The job title's department does not match the given department.")

        return data


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = StaffCustomHyperlinkedIdentityField(view_name='staff_api:staff_profile', read_only = True)
    staff_profile = CustomHyperlinkedRelatedField(view_name='org_api:staff-detail', read_only=True) #fix this url
    
    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'staff_profile', 'profile_picture']

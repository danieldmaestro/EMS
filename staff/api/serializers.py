from rest_framework import serializers
from staff.models import Query, Staff, UserProfile
from rest_framework.reverse import reverse


class CustomHyperlink(serializers.HyperlinkedRelatedField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'org_slug': request.user.staff.organization.slug,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'organization__slug': view_kwargs['org_slug'],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
    

class CustomHyperlinkIdentity(serializers.HyperlinkedIdentityField, CustomHyperlink):
    pass


class OrgCustomHyperlink(serializers.HyperlinkedRelatedField):

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
    
class OrgCustomHyperlinkIdentity(serializers.HyperlinkedIdentityField, CustomHyperlink):
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
    url = CustomHyperlinkIdentity(view_name="org_api:query-detail", read_only=True)
    organization = OrgCustomHyperlink(view_name='org_api:organization-detail', read_only=True)
    staff = CustomHyperlink(view_name='org_api:staff-detail', read_only=True)
    query_requester = CustomHyperlink(view_name='org_api:staff-detail', read_only=True)
    staff_fname = serializers.CharField(write_only=True)
    query_requester_fname = serializers.CharField(write_only=True)
    
    class Meta:
        model = Query
        fields = ['url', 'id', 'staff', 'query_requester', 'reason', 'response',
                'organization', 'is_responded', 'staff_fname', 'query_requester_fname']


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlinkIdentity(view_name="org_api:staff-detail", read_only=True)
    dept = CustomHyperlink(view_name='org_api:department-detail', read_only=True)
    organization = OrgCustomHyperlink(view_name='org_api:organization-detail', read_only=True)
    job_title = CustomHyperlink(view_name="org_api:job-title-detail", read_only=True)
    dept_name = serializers.CharField(write_only=True)
    job_title_role = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['url', 'id', 'first_name', 'last_name', 'personal_email', 'work_email', 'gender','username', 'phone_number',
                   'date_of_birth', 'state_of_origin', 'staff_status', 'next_of_kin_name', 'next_of_kin_email', 
                   'next_of_kin_phone_number', 'dept', 'dept_name', 'job_title', 'job_title_role', 'organization', 'date_employed']
        

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = OrgCustomHyperlinkIdentity(view_name='staff_api:staff_profile', read_only = True)
    staff_profile = CustomHyperlink(view_name='org_api:staff-detail', read_only=True) #fix this url
    
    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'staff_profile', 'profile_picture']

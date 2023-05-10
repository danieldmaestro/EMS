from rest_framework import serializers
from ..models import Organization, Department, JobTitle
from staff.models import Staff
from staff.api.serializers import CustomHyperlink, CustomHyperlinkIdentity, OrgCustomHyperlinkIdentity, OrgCustomHyperlink



class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    url = OrgCustomHyperlinkIdentity(view_name="org_api:organization-detail", read_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'url', 'name', 'address', 'admin_fname', 'admin_lname', 'admin_email', 
                  'admin_username', 'admin_phone_number', 'company_email_domain', 'password1', 'password2']
        
    def validate(self, data):
        """Check that the passwords match"""
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("Passwords don't match")

        return data


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlinkIdentity(view_name="org_api:department-detail", read_only=True)
    organization = OrgCustomHyperlink(view_name='org_api:organization-detail', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'url', 'name', 'description', 'slug', 'organization']


class JobTitleSerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlinkIdentity(view_name="org_api:job-title-detail", read_only=True)
    department = CustomHyperlink(view_name='org_api:department-detail', read_only=True)
    organization = OrgCustomHyperlink(view_name='org_api:organization-detail', read_only=True)
    dept_name = serializers.CharField(write_only=True)

    class Meta:
        model = JobTitle
        fields = ['id', 'url', 'role', 'description', 'department', 'dept_name', 'organization']
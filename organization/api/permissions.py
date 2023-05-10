from rest_framework import permissions

class IsPartOfOrg(permissions.BasePermission):
    """
    Custom permission to only allow users that are part of the organization
    to access the endpoint.
    """
    def has_permission(self, request, view):
        org_slug = view.kwargs['org_slug']
        return org_slug == request.user.organization.slug
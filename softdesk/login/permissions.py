from rest_framework import permissions
from api.models import Contributors

class IsSuperUser(permissions.BasePermission):
    """ Give the permission to CRUD any object if he is a Superuser"""
    def has_permission(self, request, view):

        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    """ Give permission to Read/Update/Delete an object if a user is the author of it """

    def has_object_permission(self, request, view, obj):

        return obj.auth_user_id == request.user


class IsContributor(permissions.BasePermission):
    """ Give permission to access a project if a user is a contributor """

    def has_permission(self, request, view):
        if request.user.id is None:
            return False

        project_id = str(request).split("/")[3]
        if not project_id.isalnum():
            return True

        contributors_ids = [contrib.user_id.id for contrib in Contributors.objects.filter(project_id=project_id)]

        return int(str(request.user.id)) in contributors_ids


from rest_framework import permissions
from api.models import Contributors, Project


class IsSuperUser(permissions.BasePermission):
    """ Give the permission to CRUD any object if he is a Superuser"""

    def has_permission(self, request, view):

        return request.user.is_superuser


class IsOwnerList(permissions.BasePermission):
    """ Give permission to Read a list of object if a user is the author of it """

    message = 'You should be the author of the project in order to add contributors'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        project_id = str(request).split("/")[3]
        project_ref = Project.objects.get(id=project_id)

        return project_ref.auth_user_id == request.user


class IsOwner(permissions.BasePermission):
    """ Give permission to Read/Update/Delete an object if a user is the author of it """

    message = 'You should be the author in order to access this ressources'

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        try:
            return obj.auth_user_id == request.user
        except:
            return obj.project_id.auth_user_id == request.user


class IsContributor(permissions.BasePermission):
    """ Give permission to access a project if a user is a contributor """

    message = 'You should be a contributor in order to access this ressources'

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        project_id = [v for v in str(request).split('/') if v.isnumeric()][0]

        if not project_id.isalnum():
            return True

        contributors_ids = [contrib.user_id.id for contrib in Contributors.objects.filter(project_id=project_id)]

        return int(str(request.user.id)) in contributors_ids


class UserPermission(permissions.BasePermission):

    message = 'You should be a contributor in order to access this ressources'

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        project_id = [v for v in str(request).split('/') if v.isnumeric()][0]

        if not project_id.isalnum():
            return True
        contributors_ids = [contrib.user_id.id for contrib in Contributors.objects.filter(project_id=project_id)]

        if view.action == 'list':
            return int(str(request.user.id)) in contributors_ids
        elif view.action == 'create':
            return int(str(request.user.id)) in contributors_ids
        elif view.action in ['retrieve']:
            return int(str(request.user.id)) in contributors_ids
        elif view.action in [ 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        if not request.user.is_authenticated:
            return False

        try:
            project_ref = obj.auth_user_id
        except:
            project_ref = obj.project_id.auth_user_id

        project_id = [v for v in str(request).split('/') if v.isnumeric()][0]

        if not project_id.isalnum():
            return True
        contributors_ids = [contrib.user_id.id for contrib in Contributors.objects.filter(project_id=project_id)]

        if view.action == 'retrieve':
            return int(str(request.user.id)) in contributors_ids
        elif view.action in ['update', 'partial_update']:
            return project_ref == request.user
        elif view.action == 'destroy':
            return project_ref == request.user
        else:
            return False




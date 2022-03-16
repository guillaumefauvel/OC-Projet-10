from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from api.models import Contributors, Project
from api.exceptions import ProjectExeption
from rest_framework.authtoken.models import Token
import re


class ValidToken(permissions.BasePermission):
    """ Check if the token correspond to auth user """

    def has_permission(self, request, view):

        regex = re.compile('^HTTP_')
        header_infos = dict((regex.sub('', header), value) for (header, value)
             in request.META.items() if header.startswith('HTTP_'))
        try:
            token = header_infos['AUTHORIZATION'].split()[1]
        except KeyError:
            return False

        return Token.objects.get(user=request.user) == Token.objects.get(key=token)


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
        try:
            project_ref = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            raise ProjectExeption()

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
    """
    Give the permission to the listview if the authenticated user is in the contributors list of a given project.
    The user with a Contributor status can access the detailled view item of any given item.
    If the user is a Moderator he can update a specific item but cannot delete it.
    In order to delete an item the user should be the author of it.
    """
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
        elif view.action == 'retrieve':
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
        moderators_ids = [contrib.user_id.id for contrib in Contributors.objects.filter(project_id=project_id)
                          if contrib.permission == 'Moderator']

        if view.action == 'retrieve':
            return int(str(request.user.id)) in contributors_ids
        elif view.action in ['update', 'partial_update']:
            return (project_ref == request.user) or (request.user.id in moderators_ids)
        elif view.action == 'destroy':
            return project_ref == request.user
        else:
            return False




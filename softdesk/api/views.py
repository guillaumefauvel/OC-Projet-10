from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.contrib.auth.models import User

from .models import Contributors, Project, Issue, Comment
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    UserChoiceSerializer,
    ContributorDetailSerializer,
)

from login.permissions import IsOwner, IsContributor, IsSuperUser

class ReadWriteSerializerMixin(object):
    """
    Overrides get_serializer_class to choose the read serializer
    for GET requests and the write serializer for POST requests.

    Set read_serializer_class and write_serializer_class attributes on a
    viewset.
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
            "'%s' should either include a `read_serializer_class` attribute,"
            "or override the `get_read_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
            "'%s' should either include a `write_serializer_class` attribute,"
            "or override the `get_write_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.write_serializer_class


class MultipleSerializerMixin:
    """
    Mixin that allow the use of a detailled serializer class
    """

    detail_serializer_class = None

    def get_serializer_class(self):

        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a User object representation, list and detailled view.
    It return every User object.
    """


    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):

        return User.objects.all()


class ProjectAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Project object representation, list and detailled view
    It return every Project object.

    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsContributor]


    def get_queryset(self):

        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)


class IssueAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue object.
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):

        return Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)


class CommentAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Comment object.
    """

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):

        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)


class ProjectUserView(ReadWriteSerializerMixin, ModelViewSet):
    """
    View that return a two different serializers ( READ, and WRITE wich offer the possibility to select
    a User in order to create a contribution relationship )
    It return every Contributor attached to the selected Project.
    """

    read_serializer_class = UserListSerializer
    write_serializer_class = UserChoiceSerializer
    permission_classes = [IsOwner or IsContributor]

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=self.project_id)

        return contributors

    def perform_create(self, serializer):

        project_ref = str(self.request).split("/")[3]
        serializer.save(project_id=Project.objects.get(id=int(project_ref)))


class ProjectUserDetailView(RetrieveUpdateDestroyAPIView, ModelViewSet):
    """
    View that return the view of a contribution relation object.
    """

    # TODO - Appliquer le principe DRY au possible

    serializer_class = ContributorDetailSerializer
    http_method_names = ['get', 'head', 'delete']
    permission_classes = [IsContributor]

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = [contrib.id for contrib in Contributors.objects.filter(project_id=self.project_id)]

        self.contribution = str(self.request).split("/")[5]

        if int(self.contribution) in contributors:

            contributor_user = Contributors.objects.get(id=self.contribution)

            return [contributor_user]

        return [] # TODO Lever exception -> Utilisateur non contributeur ou Inexistant

    def get_object(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=self.project_id)

        contributors = [contrib.id for contrib in contributors]

        self.contribution = str(self.request).split("/")[5]

        contributor_user = Contributors.objects.get(id=self.contribution)

        return contributor_user


class ProjectIssueView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue attached to the selected Project.
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsOwner, IsContributor]

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = Issue.objects.filter(project_id=self.project_id)

        return issues

    def perform_create(self, serializer):

        serializer.save(auth_user_id=self.request.user)
        project_ref = ''.join([s for s in str(self.request) if s.isdigit()])
        serializer.save(project_id=Project.objects.get(id=int(project_ref)))


class ProjectCommentView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Comment object representation, list and detailled view
    It return every Comment attached to the selected Issue.
    """

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsOwner, IsContributor]

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = [issue.id for issue in Issue.objects.filter(project_id=self.project_id)]

        self.issue_id = str(self.request).split("/")[5]

        if int(self.issue_id) in issues:
            comments = Comment.objects.filter(issue_id=self.issue_id)
            return comments

        return []

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)
        issue_ref = str(self.request).split("/")[5]
        serializer.save(issue_id=Issue.objects.get(id=int(issue_ref)))
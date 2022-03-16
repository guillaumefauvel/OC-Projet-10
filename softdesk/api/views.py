from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes

from .exceptions import ProjectExeption
from .models import Contributors, Project, Issue, Comment
from login.models import User

from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    ContributionFormCreator,
    AdminCommentDetailSerializer,
    ContributorSynthetic,
)

from login.permissions import IsOwner, IsOwnerList, IsContributor, IsSuperUser, UserPermission, ValidToken

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


@permission_classes([IsSuperUser, ValidToken])
class UserAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a User object representation, list and detailled view.
    It return every User object.
    """

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    http_method_names = ['get', 'head', 'delete']

    def get_queryset(self):

        return User.objects.all()


@permission_classes([IsOwner|UserPermission, ValidToken])
class ProjectAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Project object representation, list and detailled view
    It return every Project object.
    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):

        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)
        Contributors.objects.create(
            user_id=self.request.user,
            project_id=Project.objects.latest(),
            permission='Contributor',
            role='Author'
        )


@permission_classes([IsSuperUser, ValidToken])
class IssueAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue object.
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        return Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)


@permission_classes([IsSuperUser, ValidToken])
class CommentAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Comment object.
    """

    serializer_class = AdminCommentDetailSerializer
    http_method_names = ['get', 'head', 'delete']

    def get_queryset(self):

        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(auth_user_id=self.request.user)

@permission_classes([IsOwnerList, ValidToken])
class ProjectUserView(ReadWriteSerializerMixin, ModelViewSet):
    """
    View that return a two different serializers ( READ, and WRITE wich offer the possibility to select
    a User in order to create a contribution relationship )
    It return every Contributor attached to the selected Project.
    """

    read_serializer_class = ContributorSynthetic
    write_serializer_class = ContributionFormCreator

    def get_queryset(self):

        try:
            contributors = Contributors.objects.filter(project_id=self.args[0])
        except Exception as e:
            raise NotFound()
        if not contributors:
            raise NotFound()
        return contributors

    def perform_create(self, serializer):

        serializer.save(project_id=Project.objects.get(id=self.args[0]))


@permission_classes([IsOwnerList, ValidToken])
class ProjectUserDetailView(RetrieveUpdateDestroyAPIView, ModelViewSet):
    """
    View that return the view of a contribution relation object.
    """
    serializer_class = ContributorSynthetic
    http_method_names = ['get', 'head', 'delete', 'put']

    def get_queryset(self):

        try:
            contributor_user = Contributors.objects.get(id=self.args[1])
            return [contributor_user]
        except:
            raise NotFound()

    def get_object(self):

        contributor_user = Contributors.objects.get(id=self.args[1])

        return contributor_user


@permission_classes([IsOwner|UserPermission, ValidToken])
class ProjectIssueView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue attached to the selected Project.
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        id_refs = [v for v in str(self.request).split('/') if v.isnumeric()]

        issues = Issue.objects.filter(project_id=id_refs[0])

        if not issues:
            try:
                Project.objects.get(id=id_refs[0])
                raise NotFound()
            except ObjectDoesNotExist:
                raise ProjectExeption
        return issues

    def perform_create(self, serializer):

        id_refs = [v for v in str(self.request).split('/') if v.isnumeric()]
        serializer.save(auth_user_id=self.request.user)
        serializer.save(project_id=Project.objects.get(id=id_refs[0]))


@permission_classes([IsOwner|UserPermission, ValidToken])
class ProjectCommentView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Comment object representation, list and detailled view
    It return every Comment attached to the selected Issue.
    """

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        id_refs = [v for v in str(self.request).split('/') if v.isnumeric()]
        issues = [issue.id for issue in Issue.objects.filter(project_id=id_refs[0])]

        if int(id_refs[1]) in issues:
            comments = Comment.objects.filter(issue_id=id_refs[1])
            return comments
        try:
            Project.objects.get(id=id_refs[0])
            raise NotFound()
        except ObjectDoesNotExist:
            raise ProjectExeption

    def perform_create(self, serializer):

        id_refs = [v for v in str(self.request).split('/') if v.isnumeric()]

        serializer.save(auth_user_id=self.request.user)
        serializer.save(issue_id=Issue.objects.get(id=id_refs[1]))

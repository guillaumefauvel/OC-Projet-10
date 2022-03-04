from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .models import User, Contributors, Project, Issue, Comment
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

    def get_queryset(self):

        return User.objects.all()


class ProjectAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Project object representation, list and detailled view
    It return every Project object.

    """

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):

        return Project.objects.all()


class IssueAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue object.

    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        return Issue.objects.all()


class CommentAPIView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Comment object.

    """

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        return Comment.objects.all()


class ProjectUserView(ReadWriteSerializerMixin, ModelViewSet):
    """
    View that return a two different serializers ( READ, and WRITE wich offer the possibility to select
    a User in order to create a contribution relationship )
    It return every Contributor attached to the selected Project.

    """

    read_serializer_class = UserListSerializer
    write_serializer_class = UserChoiceSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer

        contributors = Contributors.objects.filter(project_id=self.project_id)
        contributors_user = [User.objects.get(id=contrib.user_id) for contrib in contributors]

        return contributors_user



class ProjectUserDetailView(RetrieveUpdateDestroyAPIView, ModelViewSet):
    """
    View that return the view of a contribution relation object.
    """

    # TODO - Appliquer le principe DRY au possible

    serializer_class = ContributorDetailSerializer
    http_method_names = ['get', 'head', 'delete']

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = [contrib.user_id for contrib in Contributors.objects.filter(project_id=self.project_id)]
        self.user_id = str(self.request).split("/")[5]

        if int(self.user_id) in contributors:
            contributor_user = Contributors.objects.filter(user_id=self.user_id).get(project_id=self.project_id)
            return [contributor_user]

        return [] # TODO Lever exception -> Utilisateur non contributeur ou Inexistant

    def get_object(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=self.project_id)
        contributors = [contrib.user_id for contrib in contributors]
        self.user_id = str(self.request).split("/")[5]

        contributor_user = Contributors.objects.filter(user_id=self.user_id).get(project_id=self.project_id)

        return contributor_user


class ProjectIssueView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Issue object representation, list and detailled view
    It return every Issue attached to the selected Project.
    """

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = Issue.objects.filter(project_id=self.project_id)

        return issues


class ProjectCommentView(MultipleSerializerMixin, ModelViewSet):
    """
    View that return two types a Comment object representation, list and detailled view
    It return every Comment attached to the selected Issue.
    """

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = [issue.id for issue in Issue.objects.filter(project_id=self.project_id)]

        self.issue_id = str(self.request).split("/")[5]

        if int(self.issue_id) in issues:
            comments = Comment.objects.filter(issue_id=self.issue_id)
            return comments

        return []

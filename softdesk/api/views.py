from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .models import User, Contributors, Project, Issue, Comment
from .serializers import UserListSerializer, UserDetailSerializer, ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer, ContributorListSerializer, UserChoiceSerializer, ProjectUserDetailSerializer, ContributorDetailSerializer

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

    detail_serializer_class = None

    def get_serializer_class(self):

        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserAPIView(MultipleSerializerMixin, ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    def get_queryset(self):

        return User.objects.all()


class ProjectAPIView(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):

        return Project.objects.all()


class IssueAPIView(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        return Issue.objects.all()


class CommentAPIView(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        return Comment.objects.all()


class ProjectUserView(ReadWriteSerializerMixin, ModelViewSet):

    read_serializer_class = UserListSerializer
    write_serializer_class = UserChoiceSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer

        contributors = Contributors.objects.filter(project_id=self.project_id)
        contributors_user = [User.objects.get(id=contrib.user_id) for contrib in contributors]

        return contributors_user


# class ProjectUserDetailView(ReadWriteSerializerMixin, ModelViewSet): ## TODO Mixin Delete
#
#     # http_method_names = ['get', 'head', 'delete']
#     read_serializer_class = ProjectUserDetailSerializer
#     write_serializer_class = ProjectUserDetailSerializer
#
#     def get_queryset(self):
#
#         self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
#         contributors = Contributors.objects.filter(project_id=self.project_id)
#         contributors = [contrib.user_id for contrib in contributors]
#         self.user_id = str(self.request).split("/")[5]
#
#         if int(self.user_id) in contributors:
#
#             contributor_user = User.objects.get(id=self.user_id)
#             return [contributor_user]
#
#         return [] # TODO Lever exception -> Utilisateur non contributeur ou Inexistant


class ProjectUserDetailView(RetrieveUpdateDestroyAPIView, ReadWriteSerializerMixin, ModelViewSet): ## TODO Mixin Delete

    # TODO - Appliquer le principe DRY au possible

    http_method_names = ['get', 'head', 'delete']
    read_serializer_class = ContributorDetailSerializer
    write_serializer_class = ContributorDetailSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=self.project_id)
        contributors = [contrib.user_id for contrib in contributors]
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

class ProjectIssueView(ReadWriteSerializerMixin, ModelViewSet):

    read_serializer_class = IssueDetailSerializer
    write_serializer_class = IssueDetailSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = Issue.objects.filter(project_id=self.project_id)

        # i = Issue.objects.create()
        # result = IssueDetailSerializer(i)
        # print(result.data)

        return issues



class ProjectCommentView(ReadWriteSerializerMixin, ModelViewSet):

    read_serializer_class = CommentListSerializer
    write_serializer_class = CommentDetailSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        issues = [issue.id for issue in Issue.objects.filter(project_id=self.project_id)]

        self.issue_id = str(self.request).split("/")[5]

        if int(self.issue_id) in issues:
            comments = Comment.objects.filter(issue_id=self.issue_id)
            return comments

        return []

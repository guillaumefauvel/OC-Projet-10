from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets

from .models import User, Contributors, Project, Issue, Comment
from .serializers import UserListSerializer, UserDetailSerializer, ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer, ContributorListSerializer, UserChoiceSerializer


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


class ProjectUserView(ModelViewSet):

    serializer_class = UserListSerializer

    def get_queryset(self):

        project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=project_id)
        contributors_user = [User.objects.get(id=user.id) for user in contributors]

        return contributors_user

    def post(self, request, format=None):
        serializer = UserChoiceSerializer(value=1)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyModelViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):

    read_serializer_class = UserListSerializer
    write_serializer_class = UserChoiceSerializer

    def get_queryset(self):

        self.project_id = str(self.request).split("/")[3]  # TODO - à améliorer
        contributors = Contributors.objects.filter(project_id=self.project_id)
        contributors_user = [User.objects.get(id=user.id) for user in contributors]

        return contributors_user

    def post(self, request, format=None):

        serializer = UserChoiceSerializer(context={'projet_id': self.project_id})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
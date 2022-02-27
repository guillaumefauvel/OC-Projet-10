from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User, Project, Issue, Comment
from .serializers import UserListSerializer, UserDetailSerializer, ProjectListSerializer, ProjectDetailSerializer,\
    IssueListSerializer, IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer


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


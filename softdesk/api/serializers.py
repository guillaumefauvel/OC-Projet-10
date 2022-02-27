from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User, Project, Issue, Comment


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name']


class UserDetailSerializer(ModelSerializer):

    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'projects']

    def get_projects(self, instance):
        queryset = instance.projects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type', 'auth_user_id', 'created_time']


class ProjectDetailSerializer(ModelSerializer):

    issues_project = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'auth_user_id', 'created_time', 'issues_project']

    def get_issues_project(self, instance):
        queryset = instance.issues_project.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'tag', 'priority', 'status', 'project_id', 'auth_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    issue_comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['title', 'tag', 'priority', 'desc', 'status',
                  'project_id', 'auth_user_id', 'created_time', 'issue_comments']

    def get_issue_comments(self, instance):
        queryset = instance.issue_comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['issue_id', 'comment_id', 'author_user_id', 'created_time']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['issue_id', 'comment_id', 'desc', 'author_user_id', 'created_time']
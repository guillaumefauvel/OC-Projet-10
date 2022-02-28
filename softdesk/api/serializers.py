from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User, Contributors, Project, Issue, Comment


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UserDetailSerializer(ModelSerializer):

    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'projects']

    def get_projects(self, instance):
        queryset = instance.projects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title','description', 'type', 'auth_user_id', 'created_time']


class ProjectDetailSerializer(ModelSerializer):

    issues_project = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'auth_user_id', 'created_time', 'issues_project']

    def get_issues_project(self, instance):
        queryset = instance.issues_project.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority', 'status', 'project_id', 'auth_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    issue_comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority', 'desc', 'status',
                  'project_id', 'auth_user_id', 'created_time', 'issue_comments']

    def get_issue_comments(self, instance):
        queryset = instance.issue_comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'description','author_user_id', 'created_time']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'description', 'author_user_id', 'created_time']
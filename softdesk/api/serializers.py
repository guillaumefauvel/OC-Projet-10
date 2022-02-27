from rest_framework.serializers import ModelSerializer

from .models import User, Project, Issue, Comment


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name']

class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type', 'auth_user_id', 'created_time']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'auth_user_id', 'created_time']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'tag', 'priority', 'status', 'project_id', 'auth_user_id', 'created_time']


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['title', 'tag', 'priority', 'desc', 'status', 'project_id', 'auth_user_id', 'created_time']


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['issue_id', 'comment_id', 'author_user_id', 'created_time']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['issue_id', 'comment_id', 'desc', 'author_user_id', 'created_time']


from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from login.models import User
from .models import Contributors, Project, Issue, Comment


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserDetailSerializer(ModelSerializer):

    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'projects']

    def get_projects(self, instance):
        queryset = instance.projects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data


class ContributionFormCreator(ModelSerializer):

    PERMISSION_CHOICES = (
        ('Moderator','Moderator'),
        ('Contributor','Contributor'),
    )

    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    permission = serializers.ChoiceField(choices=PERMISSION_CHOICES)

    class Meta:
        model = Contributors
        fields = ['user_id', 'permission', 'role', 'project_id']
        read_only_fields = ['project_id']


class ContributorSynthetic(ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'username', 'permission', 'role']
        read_only_fields = ['id', 'user_id', 'username']

    def get_username(self, instance):

        query = User.objects.get(id=instance.user_id.id)

        return query.username


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title','description', 'type', 'auth_user_id', 'created_time']
        read_only_fields = ['auth_user_id']


class ProjectDetailSerializer(ModelSerializer):

    issues_project = serializers.SerializerMethodField()
    contrib_project = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'auth_user_id',
                  'created_time', 'contrib_project', 'issues_project']

    def get_issues_project(self, instance):
        queryset = instance.issues_project.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_contrib_project(self, instance):
        queryset = instance.contrib_project.all()
        serializer = ContributorSynthetic(queryset, many=True)
        return serializer.data


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority', 'status',
                  'project_id', 'auth_user_id', 'assignee_user', 'created_time']
        read_only_fields = ['project_id', 'auth_user_id', 'assignee_user']


class IssueDetailSerializer(ModelSerializer):

    issue_comments = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField('get_project_id')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag',
                  'priority', 'desc', 'status',
                  'project_id', 'assignee_user',
                  'auth_user_id', 'created_time',
                  'issue_comments']

    def get_project_id(self, obj):

        return obj.project_id.id

    def get_issue_comments(self, instance):
        queryset = instance.issue_comments.all()
        serializer = CommentListSerializer(queryset, many=True, context={'request': self.instance})

        return serializer.data


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'auth_user_id', 'created_time', 'description']
        read_only_fields = ['auth_user_id']


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'auth_user_id', 'created_time', 'description']

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, HyperlinkedIdentityField
from rest_framework import serializers

from login.models import User

from .models import Contributors, Project, Issue, Comment

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email']


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ContributorsListSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'permission', 'role']


class UserChoiceSerializer(ModelSerializer):

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


class UserDetailSerializer(ModelSerializer):

    projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'projects']

    def get_projects(self, instance):
        queryset = instance.projects.all()
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data


class ProjectUserDetailSerializer(ModelSerializer):

    issue_comments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'issue_comments']

    def get_issue_comments(self, instance):

        project = str(self.context['request']).split()[2].split('/')[3] # TODO A changer
        issues = Issue.objects.filter(auth_user_id=instance.id)
        issues = [issue for issue in issues if issue.project_id.id == int(project)]

        serializer = IssueListSerializer(issues, many=True)

        return serializer.data


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission']


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'permission', 'role']


class ContributorSynthetic(ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ['user_id', 'username', 'permission', 'role']

    def get_username(self, instance):

        query = User.objects.get(id=instance.user_id.id)
        fullname = query.first_name + "" + query.last_name

        return fullname


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
                  'project_id', 'auth_user_id', 'assignee_user_id', 'created_time']
        read_only_fields = ['project_id', 'auth_user_id', 'assignee_user_id']


class IssueDetailSerializer(ModelSerializer):

    issue_comments = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField('get_project_id')

    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag',
                  'priority', 'desc', 'status',
                  'project_id', 'assignee_user_id',
                  'auth_user_id', 'created_time',
                  'issue_comments']

    def get_project_id(self, obj):

        return obj.project_id.id

    def get_issue_comments(self, instance):
        queryset = instance.issue_comments.all()
        serializer = CommentListSerializer(queryset, many=True, context={'request': self.instance}) # TODO
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

from django.db import models
from django.conf import settings


class Contributors(models.Model):

    PERMISSION_CHOICES = (
        ('Moderator','Moderator'),
        ('Contributor','Contributor'),
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contribution')
    project_id = models.ForeignKey('Project', null=True, on_delete=models.CASCADE, related_name='contrib_project')
    permission = models.CharField(choices=PERMISSION_CHOICES, max_length=32)
    role = models.CharField(max_length=32)

    def __str__(self):
        rep = f'Contributors({self.user_id}, {self.project_id}, {self.permission}, {self.role})'
        return rep


class Project(models.Model):

    TYPES = (
        ('Web', 'Web'),
        ('Android', 'Android'),
        ('IOS', 'IOS')
    )

    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=TYPES, max_length=32)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = ['id']

class Issue(models.Model):

    TAG_LIST = (
        ('BUG', 'BUG'),
        ('AMELIORATION', 'AMELIORATION'),
        ('TACHE', 'TACHE'),
    )

    PRIORITY_LEVEL = (
        ('Faible', 'Faible'),
        ('Moyenne', 'Moyenne'),
        ('Elevée', 'Elevée'),
    )

    STATUS_LIST = (
        ('A faire', 'A faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    )

    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    tag = models.CharField(choices=TAG_LIST, max_length=32)
    priority = models.CharField(choices=PRIORITY_LEVEL, max_length=32)
    project_id = models.ForeignKey('Project', null=True, on_delete=models.CASCADE, related_name='issues_project')
    status = models.CharField(choices=STATUS_LIST, max_length=32)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_auth')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='issues_assign')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    description = models.CharField(max_length=256)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auth_comments',null=True)
    issue_id = models.ForeignKey('Issue', null=True, on_delete=models.CASCADE, related_name='issue_comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.description)
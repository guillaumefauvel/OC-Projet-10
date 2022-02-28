from django.db import models



class User(models.Model):

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return str(self.first_name) + str(self.last_name)


class Contributors(models.Model):

    PERMISSION_CHOICES = (
        ('Author','Author'),
        ('Contributor','Contributor'),
    )

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.CharField(choices=PERMISSION_CHOICES, max_length=32)
    role = models.CharField(max_length=32)


class Project(models.Model):

    TYPES = (
        ('Web', 'Web'),
        ('Android', 'Android'),
        ('IOS', 'IOS')
    )

    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=TYPES, max_length=32)
    auth_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


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
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='issues_project', null=True)
    status = models.CharField(choices=STATUS_LIST, max_length=32)
    auth_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='issues_auth')
    assignee_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='issues_assign')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):

    description = models.CharField(max_length=256)
    author_user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='auth_comments')
    issue_id = models.ForeignKey('Issue', on_delete=models.CASCADE, related_name='issue_comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment_id)
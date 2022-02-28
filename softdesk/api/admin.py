from django.contrib import admin

from .models import User, Contributors, Project, Issue, Comment

admin.site.register(User)
admin.site.register(Contributors)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)

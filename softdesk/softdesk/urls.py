from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import (
    UserAPIView,
    ProjectAPIView,
    IssueAPIView,
    CommentAPIView,
    ProjectUserView,
    ProjectUserDetailView,
    ProjectIssueView,
    ProjectCommentView,
)

from login.views import (
    UserCreateAPIView,
    UserLoginAPIView,
    LoginView,
    UserView,
)

from django.contrib.auth import views

from login.views import CustomLoginView

router = routers.SimpleRouter()

router.register('users', UserAPIView, basename='users')
router.register('projects', ProjectAPIView, basename='projects')
router.register('issues', IssueAPIView, basename='issues')
router.register('comments', CommentAPIView, basename='comments')

project_router = routers.SimpleRouter()

project_router.register('([0-9]+)/users/([0-9]+)', ProjectUserDetailView, basename='user-project')
project_router.register('([0-9]+)/users', ProjectUserView, basename='users-project')

project_router.register('([0-9]+)/issues', ProjectIssueView, basename='issues-project')
project_router.register('([0-9]+)/issues/([0-9]+)/comments', ProjectCommentView, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserCreateAPIView.as_view(), name='signup'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('loginn/', LoginView.as_view(), name='loginn'),
    path('userss/', UserView.as_view(), name='userss'),
    path('loginnn/', CustomLoginView.as_view()),

    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/projects/', include(project_router.urls), name='project'),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import UserAPIView, ProjectAPIView, IssueAPIView, CommentAPIView, ProjectUserView, MyModelViewSet

router = routers.SimpleRouter()

router.register('users', UserAPIView, basename='users')
router.register('projects', ProjectAPIView, basename='projects')
router.register('issues', IssueAPIView, basename='issues')
router.register('comments', CommentAPIView, basename='comments')

project_router = routers.SimpleRouter()
project_router.register('([0-9]+)/users', MyModelViewSet, basename='test')


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/projects/', include(project_router.urls)),

]

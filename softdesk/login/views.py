import datetime
import jwt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .serializers import UserCreateSerializer

from login.models import User

class UserCreateAPIView(CreateAPIView):

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class LogoutView(APIView):

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        logout(request)

        return response


class CustomLoginView(LoginView):

    template_name = 'admin/login.html'

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        user = authenticate(username=username, password=password)
        login(request, user)

        response = HttpResponseRedirect('/api/projects')

        return response



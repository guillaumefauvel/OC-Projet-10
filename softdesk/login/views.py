from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from rest_framework.decorators import permission_classes

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .serializers import UserCreateSerializer

from login.models import User

from api.exceptions import UserNotFound, BadPassword


class UserCreateAPIView(CreateAPIView):
    """ Allow the registration of a new user """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class LogoutView(APIView):
    """ Disconnect the user from his account """
    def get(self, request):
        logout(request)

        return Response({'Disconnected': 'You\'ve successfully logged out'})


@permission_classes([IsAuthenticated])
class SucessLogin(APIView):
    """ Informs the user that he successfully logged in """
    def get(self, request):
        return Response({'Success': 'You\'ve successfully logged in'})


class CustomLoginView(LoginView):
    """ Log a new user by checking his credentials """

    template_name = 'admin/login.html'

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise UserNotFound
        if not user.check_password(password):
            raise BadPassword

        user = authenticate(username=username, password=password)
        login(request, user)

        response = HttpResponseRedirect('/login/success')

        return response



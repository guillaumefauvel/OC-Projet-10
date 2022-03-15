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
    # queryset = User.objects.all()

class LogoutView(APIView):

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        logout(request)

        return response

def token_creator(user_object):

    payload = {
        'id': user_object.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }

    new_token = jwt.encode(payload, 'secret', algorithm='HS256')

    return new_token

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

        token = token_creator(user)

        response = HttpResponseRedirect('/api/projects')
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        user = authenticate(username=username, password=password)
        login(request, user)

        return response


def token_check_and_update(request):

    token = request.COOKIES.get('jwt')

    if not token:
        logout(request)
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        logout(request)
        raise AuthenticationFailed('Unauthenticated')
    user = User.objects.filter(id=payload['id']).first()

    if not user.id == request.user.id:
        logout(request)
        raise AuthenticationFailed('Unauthenticated')

    token = token_creator(user)
    request.COOKIES['jwt'] = token

    return

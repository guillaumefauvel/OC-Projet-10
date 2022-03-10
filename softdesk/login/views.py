import datetime
import jwt
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import FormParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
)

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
)

from login.models import User
from api.serializers import UserListSerializer

class UserCreateAPIView(CreateAPIView):

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):

        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserListSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')

        return response



from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from rest_framework.request import Request



def preprocess_request(request):
    if isinstance(request, HttpRequest):
        return Request(request, parsers=[FormParser])
    return request


# class CustomLoginView(LoginView):
#
#     template_name = 'admin/login.html'

    # @api_view(['POST'])
    # def post(self, request):
    #
    #     username = request.POST['username']
    #     password = request.POST['password']
    #
    #     print(username, password)
    #
    #
    #     user = User.objects.filter(username=username).first()
    #
    #     if user is None:
    #         raise AuthenticationFailed('User not found')
    #     if not user.check_password(password):
    #         raise AuthenticationFailed('Incorrect password!')
    #
    #     payload = {
    #         'id': user.id,
    #         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
    #         'iat': datetime.datetime.utcnow()
    #     }
    #
    #     token = jwt.encode(payload, 'secret', algorithm='HS256')
    #
    #     response = Response()
    #     response.set_cookie(key='jwt', value=token, httponly=True)
    #     response.data = {
    #         'jwt': token
    #     }
    #
    #     return response



class CustomLoginView(LoginView):

    template_name = 'admin/login.html'

    def get_response(self):

        orginal_response = super().get_response()
        mydata = {"message": "some message", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response

# class CustomLoginView(APIView):
#
#     template_name = 'admin/login.html'
#
#     def post(self, request, format=None):
#         data = request.data
#
#         username = data.get('username', None)
#         password = data.get('password', None)
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#
#                 return Response(status=status.HTTP_200_OK)
#             else:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

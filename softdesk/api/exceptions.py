from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    status_code = 404
    default_detail = 'This user doesn\'t exist'
    default_code = '4026'


class BadPassword(APIException):
    status_code = 401
    default_detail = 'Incorrect password'
    default_code = '4026'


class ProjectException(APIException):
    status_code = 404
    default_detail = 'This project doesn\'t exist'
    default_code = '4026'


class TokenException(APIException):
    status_code = 401
    default_detail = 'The token you provided is invalid'
    default_code = '4027'


class MissingTokenException(APIException):
    status_code = 401
    default_detail = 'You didn\'t provide any token'
    default_code = '4028'

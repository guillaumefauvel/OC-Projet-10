from rest_framework.exceptions import APIException

class ProjectExeption(APIException):
    status_code = 404
    default_detail = 'This project doest not exist'
    default_code = '4026'

from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException


class CustomException(APIException):
    """ Custom exception class to comply with pytests """
    detail = None
    status_code = None

    def __init__(self, status_code, message):
        CustomException.status_code = status_code
        CustomException.detail = message


class ListCreateDestroyViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin):
    pass
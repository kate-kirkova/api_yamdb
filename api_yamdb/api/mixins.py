from rest_framework import viewsets, mixins


class ListCreateDestroyViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin):
    pass

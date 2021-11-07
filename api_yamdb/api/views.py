from django.core.mail import send_mail
from rest_framework import filters, generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import SlidingToken

from .permissions import AdminLevelPermission, UserAccessPermission
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          TitleSerializer, UserSerializer)
from reviews.models import User, Category, Genre, Title

class RegisterNewUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = user.confirmation_code
        send_mail(
            'Confirmation code', f'Your code: {token}', 'awesome@guy.com',
            [user.email],
            fail_silently=False,)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomJWTTokenView(generics.CreateAPIView):
    serializer_class = GetJWTTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data['username'])
        token = SlidingToken.for_user(user)

        return Response({'Token': str(token)}, status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminLevelPermission,)
    lookup_field = 'username'


class GetPersonalInfoViewSet(mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserAccessPermission,)


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

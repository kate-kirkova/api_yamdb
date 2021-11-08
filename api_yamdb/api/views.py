from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import filters, generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, SlidingToken

from reviews.models import User, Category, Genre, Title

from .permissions import (AdminLevelPermission, UserAccessPermission,
                          AdminLevelOrReadOnlyPermission)
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          TitleSerializer, UserSerializer)

class RegisterNewUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = user.confirmation_code
        send_mail(
            'Confirmation code', f'Your code: {code}', 'awesome@guy.com',
            [user.email],
            fail_silently=False,)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomJWTTokenView(generics.CreateAPIView):
    serializer_class = GetJWTTokenSerializer
    permission_classes = (permissions.AllowAny,)

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

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request):
        if request.method == 'GET':
            user = User.objects.filter(id=request.user.id)
            serializer = self.get_serializer(user, many=True)
        elif request.method == 'PATCH':
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data) 


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminLevelOrReadOnlyPermission,)

    def perform_create(self, serializer):
        category = generics.get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminLevelOrReadOnlyPermission,)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminLevelOrReadOnlyPermission,)

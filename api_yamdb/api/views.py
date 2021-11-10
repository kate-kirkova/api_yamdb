from django.core.mail import send_mail
from rest_framework import filters, generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import SlidingToken

from reviews.models import User, Category, Genre, Title

from .permissions import (AdminLevelPermission, UserAccessPermission,
                          AdminLevelOrReadOnlyPermission)
from .serializers import (AdminCreateUserFullSerializer, AdminCreateUserSerializer, CategorySerializer, CreateUserSerializer,
                          GenreSerializer, GetJWTTokenSerializer,
                          TitleSerializer, UserSerializer, UserWithAdminAccessSerializer)


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
    permission_classes = (AdminLevelPermission, permissions.IsAuthenticated)
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminCreateUserFullSerializer
        else:
            return UserWithAdminAccessSerializer


class UserDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if self.get_queryset():
            user = self.get_queryset()
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        return Response(status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        instance = request.user
        if instance.is_superuser:
            serializer = UserWithAdminAccessSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = UserSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = self.get_queryset()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return User.objects.get(username=self.request.user)
    


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

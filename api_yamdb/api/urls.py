from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    RegisterNewUserAPIView, CustomJWTTokenView, UserViewSet)


app_name = 'api'

router = SimpleRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegisterNewUserAPIView.as_view()),
    path('v1/auth/token/', CustomJWTTokenView.as_view()),
]

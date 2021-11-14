from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                    RegisterNewUserAPIView, CustomJWTTokenView, UserViewSet,
                    ReviewViewSet, CommentViewSet)


app_name = 'api'

router = SimpleRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegisterNewUserAPIView.as_view()),
    path('v1/auth/token/', CustomJWTTokenView.as_view()),
]

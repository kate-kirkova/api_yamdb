from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet


app_name = 'api'

router = SimpleRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]

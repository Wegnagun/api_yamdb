from django.urls import include, path
from rest_framework import routers
from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('category', CategoryViewSet, basename='category')


urlpatterns = [
    path('v1/', include(router.urls))
]

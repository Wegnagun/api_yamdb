from django.urls import include, path
from rest_framework import routers

from .views import (APICreateToken, APISignUp, CategoryViewSet, GenreViewSet,
                    TitleViewSet)

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('category', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', APISignUp.as_view(), name='signup'),
    path('auth/token/', APICreateToken.as_view(), name='token')
]

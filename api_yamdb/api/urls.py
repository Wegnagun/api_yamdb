from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet
from .views import (CategoryViewSet, CommentViewSet, CreateToken, GenreViewSet,
                    ReviewViewSet, SignUp, TitleViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='category')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp, name='signup'),
    path('v1/auth/token/', CreateToken, name='token')
]

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, decorators
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review
from users.models import CustomUser
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAuthorOrReadOnly, IsRoleModerator,
                          IsAdminOrReadOnly, IsRoleAdmin)
from .serializers import (CategorySerializer, CreateTokenSerializer,
                          GenreSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleCreateSerializer,
                          CommentSerializer, ReviewSerializer)


def send_email(user, code):
    email = EmailMessage(
        subject='Код подтвержения для доступа к API!',
        body=code,
        to=[user.email, ]
    )
    email.send()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg("reviews__score"))
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleReadSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


@decorators.api_view(['POST'])
def SignUp(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    code = default_token_generator.make_token(user)
    send_email(user, code)
    return Response(serializer.data, status=status.HTTP_200_OK)


@decorators.api_view(['POST'])
def CreateToken(request):
    try:
        if 'username' in request.data:
            user = get_object_or_404(
                CustomUser.objects, username=request.data['username'])
        serializer = CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
    except CustomUser.DoesNotExist:
        return Response(
            {'username': 'Пользователь не найден!'},
            status=status.HTTP_404_NOT_FOUND)

    if default_token_generator.check_token(user, data['confirmation_code']):
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')))

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                id=self.kwargs.get('review_id'),
                title=self.kwargs.get('title_id')))

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')).comments.all()

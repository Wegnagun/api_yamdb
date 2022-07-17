import uuid

from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from reviews.models import Category, Genre, Title, MyOwnUser, Review
from .filters import TitleFilter
from .permissions import (IsAuthorOrReadOnly, IsRoleAdmin, IsRoleModerator,
                          ReadOnly)
from .serializers import (CategorySerializer, CreateTokenSerializer,
                          GenreSerializer, SignUpSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer,
                          AdminUserSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.all().annotate
                (Avg("reviews__score")).order_by('name'))
    serializer_class = TitleSerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsRoleAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class APISignUp(views.APIView):
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.username == 'me':
            return Response('Нельзя создавать пользователя с таким именем',
                            status=status.HTTP_400_BAD_REQUEST)
        email_body = (
            f'Код подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APICreateToken(views.APIView):
    def post(self, request):
        if self.request.method == 'POST':
            if 'username' in request.data:
                get_object_or_404(
                    MyOwnUser.objects, username=request.data['username'])
        serializer = CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = MyOwnUser.objects.get(username=data['username'])
        except MyOwnUser.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     serializer = CreateTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = get_object_or_404(
    #         MyOwnUser,
    #         username=serializer.validated_data['username']
    #     )
    #     if serializer.validated_data['conf_code'] != user.conf_code:
    #         return Response(
    #             {'conf_code': 'Несовпадают коды!'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return Response(
    #         {'token': str(RefreshToken.for_user(user).access_token)},
    #         status=status.HTTP_200_OK
    #     )


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyOwnUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def about_me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

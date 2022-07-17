import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from .filters import TitleFilter
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, MyOwnUser, Review
from .permissions import (IsAdminOrReadOnly, IsOwnerOrStaffOrReadOnly,
                          IsRoleAdmin)
from .serializers import (CategorySerializer, CreateTokenSerializer,
                          GenreSerializer, SignUpSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer,
                          AdminUserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_class = [filters.SearchFilter]
    lookup_field = 'slug'
    search_field = ('=name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_class = [filters.SearchFilter]
    lookup_field = 'slug'
    search_field = ('=name',)


class APISignUp(views.APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = str(uuid.uuid4())
        send_mail(
            'Ваш код подтверждения',
            confirmation_code,
            settings.DEFAULT_FROM_EMAIL,
            [serializer.validated_data.get('email')]
        )
        serializer.save(confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APICreateToken(views.APIView):

    def post(self, request):
        serializer = CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            MyOwnUser,
            username=serializer.validated_data['username']
        )
        if serializer.validated_data['conf_code'] != user.conf_code:
            return Response(
                {'conf_code': 'Несовпадают коды!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id')))

    def get_queryset(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')).reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

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

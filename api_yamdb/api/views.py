import uuid
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, MyOwnUser

from .permissons import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CreateTokenSerializer,
                          GenreSerializer, SignUpSerializer,
                          TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly
    # filterset_class =


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = IsAdminOrReadOnly
    # filterset_class =


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly
    # filterset_class =


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

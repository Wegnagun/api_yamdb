from rest_framework import viewsets
from reviews.models import Title
from .serializers import TitleSerializer
from .permissons import IsAdminOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly
    # filterset_class =


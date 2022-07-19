from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   DestroyModelMixin)

from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyViewSet(CreateModelMixin, ListModelMixin,
                               DestroyModelMixin, GenericViewSet):
    pass

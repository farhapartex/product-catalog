from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters
from catalog import models, serializers, filters as catalog_filters


class ImageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = catalog_filters.ImageFilter

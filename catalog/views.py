from rest_framework import generics, viewsets, mixins
from catalog import models, serializers


class ImageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

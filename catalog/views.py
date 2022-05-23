from rest_framework import viewsets, mixins
from rest_framework import response
from django_filters import rest_framework as filters
from catalog import models, serializers, filters as catalog_filters


class ImageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = catalog_filters.ImageFilter

    def get_serializer_context(self):
        context = super(ImageViewSet, self).get_serializer_context()
        if self.request.GET.get('size'):
            context.update({"size": self.request.GET['size']})
        return context


class ImageMetadataViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = models.ImageMetadata.objects.all()
    serializer_class = serializers.ImageMetadataSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = catalog_filters.ImageMetadataFilter
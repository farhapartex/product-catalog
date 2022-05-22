from rest_framework import serializers
from catalog import models


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ("id", "filename", "original_url", "brand_name")


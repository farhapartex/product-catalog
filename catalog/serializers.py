from PIL import ImageStat, Image
from rest_framework import serializers
from django.conf import settings
from catalog import models, constants


class ImageSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()

    def get_url(self, instance):
        image_url = None
        if "size" in self.context:
            size = self.context["size"]
            file_path = f"{settings.BASE_DIR}/media/images/{instance.directory}/{instance.filename}"
            image = Image.open(file_path)
            ratio = image.height / image.width

            if size == constants.SMALL_SIZE:
                new_height = int(ratio * constants.SMALL_WIDTH)
                image_url = f"/media/images/{instance.directory}/{instance.directory}-{256}x{new_height}.jpg" if image.width > 256 else instance.filename
            elif size == constants.MEDIUM_SIZE:
                new_height = int(ratio * constants.MEDIUM_WIDTH)
                image_url = f"/media/images/{instance.directory}/{instance.directory}-{1024}x{new_height}.jpg" if image.width > 1024 else instance.filename
            elif size == constants.LARGE_SIZE:
                new_height = int(ratio * constants.LARGE_WIDTH)
                image_url = f"/media/images/{instance.directory}/{instance.directory}-{2048}x{new_height}.jpg" if image.width > 2048 else instance.filename

            return self.context["request"].build_absolute_uri(image_url)

        image_url = f"/media/images/{instance.directory}/{instance.filename}"
        return self.context["request"].build_absolute_uri(image_url)

    def get_filename(self, instance):
        if "size" in self.context:
            size = self.context["size"]
            file_path = f"{settings.BASE_DIR}/media/images/{instance.directory}/{instance.filename}"
            image = Image.open(file_path)
            ratio = image.height / image.width

            if size == constants.SMALL_SIZE:
                new_height = int(ratio * constants.SMALL_WIDTH)
                return f"{instance.directory}-{256}x{new_height}.jpg" if image.width > 256 else instance.filename
            elif size == constants.MEDIUM_SIZE:
                new_height = int(ratio * constants.MEDIUM_WIDTH)
                return f"{instance.directory}/{instance.directory}-{1024}x{new_height}.jpg" if image.width > 1024 else instance.filename
            elif size == constants.LARGE_SIZE:
                new_height = int(ratio * constants.LARGE_WIDTH)
                return f"{instance.directory}/{instance.directory}-{2048}x{new_height}.jpg" if image.width > 2048 else instance.filename

        return instance.filename

    def get_metadata(self, instance):
        return {
            "original_height": instance.metadata_of.original_height,
            "original_width": instance.metadata_of.original_width,
            "format": instance.metadata_of.format,
            "is_animated": instance.metadata_of.is_animated
        }
    class Meta:
        model = models.Image
        fields = ("id", "url", "filename", "original_url", "brand_name", "metadata")
        extra_kwargs = {
            "metadata": {"read_only": True}
        }


class ImageMetadataSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return {
            "id": instance.image.id,
            "image-type": instance.image.image_type

        }
    class Meta:
        model = models.ImageMetadata
        fields = ("id", "image", "filename", "scrapped_at", "original_height", "original_width", "format", "is_animated", "mode", "brightness")
from django.db import models


class BaseAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(BaseAbstract):
    filename = models.CharField(max_length=300)
    original_url = models.URLField(max_length=300)
    brand_name = models.CharField(max_length=255)
    image_type = models.CharField(max_length=100)
    directory = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.id}: {self.filename}"


class ImageMetadata(BaseAbstract):
    image = models.OneToOneField(Image, related_name='metadata_of', on_delete=models.CASCADE)
    filename = models.CharField(max_length=300)
    scrapped_at = models.DateTimeField()
    original_height = models.IntegerField()
    original_width = models.IntegerField()
    format = models.CharField(max_length=100)
    is_animated = models.BooleanField()
    mode = models.CharField(max_length=100, blank=True, null=True)
    brightness = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.filename



from django.contrib import admin
from catalog import models


# Register your models here.

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "directory", "filename", "brand_name", "created_at")


@admin.register(models.ImageMetadata)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "filename", "scrapped_at", "original_height", "original_width", "format")

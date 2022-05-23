from django.urls import path, re_path, include
from rest_framework import routers
from catalog import views

router = routers.DefaultRouter()

router.register(r"^images", views.ImageViewSet, basename='image')
router.register(r"^image-metadatas", views.ImageMetadataViewSet, basename='image-metadata')

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
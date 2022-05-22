from django.dispatch import receiver
from catalog import signals
from catalog import models


@receiver(signals.create_image_metadata)
def create_image_metadata(sender, image_id, metadata, **kwargs):
    image_instance = models.Image.objects.get(id=image_id)
    models.ImageMetadata.objects.create(
        image=image_instance,
        filename=metadata["filename"],
        scrapped_at=metadata["scrapped_at"],
        original_height=metadata["original_height"],
        original_width=metadata["original_width"],
        format=metadata["format"],
        is_animated=metadata["is_animated"],
        mode=metadata["mode"],
        brightness=metadata["brightness"]
    )

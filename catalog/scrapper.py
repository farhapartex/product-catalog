import requests
import os
import uuid

from PIL import ImageStat, Image
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from catalog import models
from catalog import signals

URL = "https://unsplash.com/t/food-drink"
DIRECTORY_PATH = f"{settings.BASE_DIR}/images"


def check_path_exists_or_create():
    if not os.path.exists(DIRECTORY_PATH):
        os.makedirs(DIRECTORY_PATH)


def store_image(url):
    image_bytes = requests.get(url, allow_redirects=True)
    file_name = f"unsplash_{uuid.uuid4()}.jpg"
    file_path = f"{settings.BASE_DIR}/images/{file_name}"
    with open(file_path, "wb") as image:
        image.write(image_bytes.content)

    return file_name, file_path


def store_image_data_to_db(file_name, file_path, image_type):
    image = Image.open(file_path)
    stat = ImageStat.Stat(image.convert('L'))

    image_instance = models.Image.objects.create(
        filename=file_name,
        original_url="https://unsplash.com",
        brand_name="Unsplash",
        image_type=image_type
    )

    image_metadata = {
        "filename":file_name,
        "scrapped_at": timezone.now(),
        "original_height": image.height,
        "original_width": image.width,
        "format": image.format,
        "is_animated": getattr(image, "is_animated", False),
        "mode": image.mode,
        "brightness": stat.mean[0]
    }

    signals.create_image_metadata.send(sender="create_image_metadata", image_id=image_instance.id, metadata=image_metadata)

    # models.ImageMetadata(
    #     image=image_instance,
    #     filename=file_name,
    #     scrapped_at=timezone.now(),
    #     original_height=image.height,
    #     original_width=image.width,
    #     format=image.format,
    #     is_animated=getattr(image, "is_animated", False),
    #     mode=image.mode,
    #     brightness=stat.mean[0]
    # ).save()


def photo_scrapper():
    check_path_exists_or_create()
    request = requests.get(url=URL, allow_redirects=True)
    soup = BeautifulSoup(request.text, "html.parser")
    figures = soup.find_all('figure', itemprop="image")
    max_size = 0
    for figure in figures:
        image_tag = figure.find("img")
        selected_image_url = ""
        if image_tag is not None:
            urls = image_tag['srcset'].split(",")
            for url in urls:
                img_url, size = url.split()
                if int(size[:len(size) - 1]) > max_size:
                    selected_image_url = img_url

            file_name, file_path = store_image(selected_image_url)
            store_image_data_to_db(file_name, file_path, "food-drink")

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
SMALL_WIDTH = 256
MEDIUM_WITH = 1024
LARGE_WIDTH = 2048


def check_path_exists_or_create(path):
    if not os.path.exists(path):
        os.makedirs(path)


def store_image_by_size(file_path, new_width, ratio, image_directory, dir_unique_name):
    new_image = Image.open(file_path)
    new_height = int(ratio * new_width)
    # If the size parameter is smaller than the actual size of the image, resize it
    if new_image.width > new_width:
        new_image.thumbnail((new_width, new_height), Image.ANTIALIAS)
        new_image.save(f"{image_directory}/{dir_unique_name}-{new_width}x{new_height}.jpg")


def store_image(url):
    # pull image from the server
    image_bytes = requests.get(url, allow_redirects=True)

    # start process to save image with different sizes
    dir_unique_name = str(uuid.uuid4())
    image_directory = f"{settings.BASE_DIR}/images/{dir_unique_name}"
    check_path_exists_or_create(image_directory)
    file_name = f"unsplash-{dir_unique_name}-original.jpg"
    file_path = f"{image_directory}/{file_name}"
    with open(file_path, "wb") as image:
        image.write(image_bytes.content)

    image = Image.open(file_path)
    ratio = image.height / image.width

    for width in [SMALL_WIDTH, MEDIUM_WITH, LARGE_WIDTH]:
        store_image_by_size(file_path, width, ratio, image_directory, dir_unique_name)

    return file_name, file_path, dir_unique_name


def store_image_data_to_db(file_name, file_path, image_type, img_directory):
    image = Image.open(file_path)
    stat = ImageStat.Stat(image.convert('L'))

    image_instance = models.Image.objects.create(
        filename=file_name,
        original_url="https://unsplash.com",
        brand_name="Unsplash",
        image_type=image_type,
        directory=img_directory
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


def photo_scrapper():
    check_path_exists_or_create(DIRECTORY_PATH)
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

            file_name, file_path, img_directory = store_image(selected_image_url)
            # for now image_type is hard coded, it can be dynamic when there are more images from different source
            store_image_data_to_db(file_name, file_path, "food-drink", img_directory)

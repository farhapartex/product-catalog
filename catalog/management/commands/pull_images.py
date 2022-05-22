from django.core.management.base import BaseCommand, CommandError
from catalog import scrapper


class Command(BaseCommand):
    help = 'Pull images from server'

    def handle(self, *args, **options):
        scrapper.photo_scrapper()

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from model_bakery import baker


class Command(BaseCommand):
    def handle(self, *args, **options):
        baker.make(User, _quantity=10000)

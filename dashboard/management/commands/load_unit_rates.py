from django.core.management.base import BaseCommand

from domain import unit_rates


class Command(BaseCommand):
    help = "Load consumption"

    def handle(self, *args, **kwargs):
        unit_rates.load_unit_rates()

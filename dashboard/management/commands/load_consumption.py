from django.core.management.base import BaseCommand

from domain import consumption


class Command(BaseCommand):
    help = "Load consumption"

    def handle(self, *args, **kwargs):
        consumption.load_electricity_consumption()
        consumption.load_gas_consumption()

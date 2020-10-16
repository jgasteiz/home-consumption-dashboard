from django.core.management.base import BaseCommand

from dashboard import consumption_helpers


class Command(BaseCommand):
    help = "Load consumption"

    def handle(self, *args, **kwargs):
        consumption_helpers.load_electricity_consumption()
        consumption_helpers.load_gas_consumption()

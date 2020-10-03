import decimal

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.auth import HTTPBasicAuth

from data import models


class Command(BaseCommand):
    help = "Load consumption"

    def handle(self, *args, **kwargs):
        _get_consumption(settings.ELECTRICITY_CONSUMPTION_URL)


def _get_consumption(url: str):
    print(f"Getting consumption for {url}")
    response = requests.get(url, auth=HTTPBasicAuth(settings.API_KEY, ""),)
    for result in response.json()["results"]:
        entry, created = models.ElectricityConsumption.objects.get_or_create(
            interval_start=result["interval_start"],
            interval_end=result["interval_end"],
            consumption=decimal.Decimal(result["consumption"]),
        )
        if not created:
            print("Consumption fetched")
            return
    if response.json().get("next"):
        next_url = response.json()["next"]
        _get_consumption(next_url)
    else:
        print("Consumption fetched")

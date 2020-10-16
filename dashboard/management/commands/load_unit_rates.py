import datetime
import decimal

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.auth import HTTPBasicAuth

from data import models


class Command(BaseCommand):
    help = "Load consumption"

    def handle(self, *args, **kwargs):
        earliest_consumption = models.ElectricityConsumption.objects.earliest("interval_start")
        _get_unit_rates_until_date(
            url=settings.ELECTRICITY_RATES_URL,
            until_date=earliest_consumption.interval_start.date(),
        )


def _get_unit_rates_until_date(url: str, until_date: datetime.date):
    print(f"Getting unit rates for {url}")
    response = requests.get(url, auth=HTTPBasicAuth(settings.API_KEY, ""))
    latest_entry = None
    for result in response.json()["results"]:
        entry, created = models.UnitRate.objects.get_or_create(
            value_exc_vat=decimal.Decimal(result["value_exc_vat"]),
            value_inc_vat=decimal.Decimal(result["value_inc_vat"]),
            valid_from=result["valid_from"],
            valid_to=result["valid_to"],
        )
        if not created:
            print("Unit rates fetched")
            return
        latest_entry = entry

    if not latest_entry:
        print("Unit rates fetched")
        return

    latest_entry.refresh_from_db()
    latest_entry_valid_from = latest_entry.valid_from.date()

    if response.json().get("next") and until_date < latest_entry_valid_from:
        next_url = response.json()["next"]
        _get_unit_rates_until_date(url=next_url, until_date=until_date)
    else:
        print("Unit rates fetched")

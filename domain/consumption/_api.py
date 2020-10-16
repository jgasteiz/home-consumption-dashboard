import decimal
from typing import Union

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

from data import models

__all__ = [
    "load_electricity_consumption",
    "load_gas_consumption",
]


def load_electricity_consumption():
    """
    Load all available electricity consumption data from the Octopus Energy API.
    """
    _load_consumption_from_api(settings.ELECTRICITY_CONSUMPTION_URL, models.ElectricityConsumption)


def load_gas_consumption():
    """
    Load all available gas consumption data from the Octopus Energy API.
    """
    _load_consumption_from_api(settings.GAS_CONSUMPTION_URL, models.GasConsumption)


def _load_consumption_from_api(
    url: str,
    consumption_class: Union[
        models.ElectricityConsumption.Meta.__class__,
        models.GasConsumption.Meta.__class__,
    ],
):
    print(f"Getting consumption for {url}")
    response = requests.get(url, auth=HTTPBasicAuth(settings.API_KEY, ""))
    for result in response.json()["results"]:
        entry, created = consumption_class.objects.get_or_create(
            interval_start=result["interval_start"],
            interval_end=result["interval_end"],
            consumption=decimal.Decimal(result["consumption"]),
        )
        if not created:
            print("Consumption fetched")
            return
    if response.json().get("next"):
        next_url = response.json()["next"]
        _load_consumption_from_api(next_url, consumption_class)
    else:
        print("Consumption fetched")

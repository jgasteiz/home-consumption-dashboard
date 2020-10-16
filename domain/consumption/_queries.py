import datetime
import decimal
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta

from dailyconsumption import localtime
from data import models
from domain import unit_rates

__all__ = [
    "get_consumption_on_date",
    "get_payable_on_date",
    "get_usage_on_date",
    "get_consumption_available_dates",
    "get_previous_and_next_dates",
]


def get_consumption_on_date(date: datetime.date) -> List[dict]:
    """
    Get consumption data on a given date.
    """
    consumption_list = models.ElectricityConsumption.objects.filter(
        interval_start__gte=localtime.midnight(date),
        interval_end__lte=localtime.next_midnight(date),
    ).order_by("interval_start")
    unit_rates_on_date = unit_rates.get_unit_rates_on_date(date)
    consumption_with_unit_rate = zip(consumption_list, unit_rates_on_date)
    consumption_on_date = []
    for consumption, unit_rate in consumption_with_unit_rate:
        payable_in_pence = consumption.consumption * unit_rate.value_inc_vat
        consumption_on_date.append(
            {
                "consumption": consumption.consumption,
                "interval_start": consumption.interval_start.strftime("%H:%M"),
                "interval_end": consumption.interval_end.strftime("%H:%M"),
                "value_inc_vat": unit_rate.value_inc_vat,
                "payable_in_pence": payable_in_pence,
            }
        )
    return consumption_on_date


def get_payable_on_date(consumption_entry_list: List[dict]) -> decimal.Decimal:
    """
    Get payable in £ of a given list of consumption entries that contains the payable amount
    per entry in pence.
    """
    return sum([entry["payable_in_pence"] for entry in consumption_entry_list]) / 100


def get_usage_on_date(consumption_entry_list: List[dict]) -> decimal.Decimal:
    """
    Get usage in kWh of a given list of consumption entries that contains the usage amount
    per entry in kWh.
    """
    return sum([entry["consumption"] for entry in consumption_entry_list])


def get_consumption_available_dates() -> List[str]:
    """
    Get a list available consumption dates taken from the existing consumption data in the db.
    """
    latest_consumption = models.ElectricityConsumption.objects.latest("interval_start")
    earliest_consumption = models.ElectricityConsumption.objects.earliest("interval_start")
    date = latest_consumption.interval_start.date()
    date_list = []
    while date >= earliest_consumption.interval_start.date():
        date_list.append(date.isoformat())
        date = date - relativedelta(days=1)
    return date_list


def get_previous_and_next_dates(
    date_list: List[str], selected_date: datetime.date
) -> Tuple[Optional[str], Optional[str]]:
    """
    Return the previous and next dates of a selected date, using a list of dates as boundaries.
    """
    next_date = (selected_date + relativedelta(days=1)).isoformat()
    if next_date not in date_list:
        next_date = None
    previous_date = (selected_date - relativedelta(days=1)).isoformat()
    if previous_date not in date_list:
        previous_date = None
    return previous_date, next_date

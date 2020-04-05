import datetime
import decimal
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta

from data import models

from . import helpers


def get_unit_rates(selected_date: datetime.date) -> List[dict]:
    """
    Get a list of unit rates for the given date.
    """
    return models.UnitRate.objects.filter(
        valid_from__gte=helpers.midnight(selected_date),
        valid_from__lte=helpers.next_midnight(selected_date),
    ).order_by("valid_from")


def get_consumption_available_dates() -> List[str]:
    """
    Get a list available consumption dates taken from the existing consumption data in the db.
    """
    latest_consumption = models.Consumption.objects.latest("interval_start")
    earliest_consumption = models.Consumption.objects.earliest("interval_start")
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


def get_consumption_on_date(date: datetime.date) -> List[dict]:
    """
    Get consumption data on a given date.
    """
    consumption_list = models.Consumption.objects.filter(
        interval_start__gte=helpers.midnight(date),
        interval_end__lte=helpers.next_midnight(date),
    ).order_by("interval_start")
    return [
        {
            "consumption": decimal.Decimal(c.consumption),
            "interval_start": c.interval_start.strftime("%H:%M"),
            "interval_end": c.interval_end.strftime("%H:%M"),
        }
        for c in consumption_list
    ]


def get_usage_on_date(consumption_entry_list: List[dict]) -> decimal.Decimal:
    """
    Get usage in kWh of a given list of consumption entries.
    """
    return sum([entry["consumption"] for entry in consumption_entry_list])

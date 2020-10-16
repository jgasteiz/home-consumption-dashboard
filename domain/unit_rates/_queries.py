import datetime
from typing import List

from dailyconsumption import localtime
from data import models

__all__ = [
    "get_unit_rates_on_date",
]


def get_unit_rates_on_date(date: datetime.date) -> List[dict]:
    """
    Get a list of unit rates for the given date.
    """
    return models.UnitRate.objects.filter(
        valid_from__gte=localtime.midnight(date),
        valid_from__lte=localtime.next_midnight(date),
    ).order_by("valid_from")

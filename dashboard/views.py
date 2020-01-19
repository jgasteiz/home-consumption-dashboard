import datetime
import json
from typing import List, Optional, Tuple

import requests
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from requests.auth import HTTPBasicAuth

from data import models

from . import helpers


def unit_rates(request):
    current_time = helpers.now()
    current_date = helpers.date(current_time)
    unit_rates_list = _get_unit_rates(current_date)

    unit_rates_json = json.dumps(
        [
            {
                "valid_from": unit_rate["valid_from"].strftime("%H:%M"),
                "valid_to": unit_rate["valid_to"].strftime("%H:%M"),
                "value": unit_rate["value"],
            }
            for unit_rate in unit_rates_list
        ]
    )

    return render(
        request,
        "dashboard/unit_rates.html",
        context={
            "unit_rates_list": unit_rates_list,
            "unit_rates_json": unit_rates_json,
            "current_date": current_date.isoformat(),
            "current_time": current_time,
        },
    )


def consumption(request):
    date_list = _get_available_dates()
    selected_date = helpers.parse_date(request.GET.get("date", date_list[0]))
    previous_date, next_date = _get_previous_and_next_dates(date_list, selected_date)

    return render(
        request,
        "dashboard/consumption.html",
        context={
            "consumption_json": json.dumps(_get_consumption(selected_date)),
            "selected_date": selected_date.isoformat(),
            "next_date": next_date,
            "previous_date": previous_date,
        },
    )


def _get_unit_rates(selected_date: datetime.date) -> List[dict]:
    unit_rate_list = cache.get("unit_rates")
    if unit_rate_list:
        return unit_rate_list

    response = requests.get(
        settings.ELECTRICITY_RATES_URL, auth=HTTPBasicAuth(settings.API_KEY, ""),
    )
    response_json = response.json()
    unit_rate_list = [
        {
            "valid_from": helpers.parse_date_time(result["valid_from"]),
            "valid_to": helpers.parse_date_time(result["valid_to"]),
            "value": result["value_inc_vat"],
        }
        for result in response_json["results"]
        if helpers.parse_date_time(result["valid_from"]).date() == selected_date
    ]
    unit_rate_list.reverse()
    cache.set("unit_rates", unit_rate_list, 3600)
    return unit_rate_list


def _get_available_dates() -> List[str]:
    latest_consumption = models.Consumption.objects.latest("interval_start")
    earliest_consumption = models.Consumption.objects.earliest("interval_start")
    date = latest_consumption.interval_start.date()
    date_list = []
    while date >= earliest_consumption.interval_start.date():
        date_list.append(date.isoformat())
        date = date - helpers.relativedelta(days=1)
    return date_list


def _get_previous_and_next_dates(
    date_list: List[str], selected_date: datetime.date
) -> Tuple[Optional[str], Optional[str]]:
    next_date = (selected_date + helpers.relativedelta(days=1)).isoformat()
    if next_date not in date_list:
        next_date = None
    previous_date = (selected_date - helpers.relativedelta(days=1)).isoformat()
    if previous_date not in date_list:
        previous_date = None
    return previous_date, next_date


def _get_consumption(date: datetime.date) -> List[dict]:
    consumption_list = models.Consumption.objects.filter(
        interval_start__gte=helpers.midnight(date),
        interval_end__lte=helpers.next_midnight(date),
    ).order_by("interval_start")
    return [
        {
            "consumption": float(c.consumption),
            "interval_start": c.interval_start.strftime("%H:%M"),
            "interval_end": c.interval_end.strftime("%H:%M"),
        }
        for c in consumption_list
    ]

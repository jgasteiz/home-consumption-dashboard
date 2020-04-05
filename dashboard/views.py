import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from . import helpers, consumption_helpers


def unit_rates(request):
    current_time = helpers.now()
    current_date = helpers.date(current_time)
    unit_rates_list = consumption_helpers.get_unit_rates(current_date)

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
    date_list = consumption_helpers.get_consumption_available_dates()
    selected_date = helpers.parse_date(request.GET.get("date", date_list[0]))
    previous_date, next_date = consumption_helpers.get_previous_and_next_dates(date_list, selected_date)

    consumption_on_date = consumption_helpers.get_consumption_on_date(selected_date)
    usage_on_date = consumption_helpers.get_usage_on_date(consumption_on_date)

    return render(
        request,
        "dashboard/consumption.html",
        context={
            "usage_on_date": usage_on_date,
            "consumption_json": json.dumps(consumption_on_date, cls=DjangoJSONEncoder),
            "selected_date": selected_date.isoformat(),
            "next_date": next_date,
            "previous_date": previous_date,
        },
    )

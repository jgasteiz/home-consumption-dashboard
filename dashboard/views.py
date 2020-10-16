import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from dailyconsumption import localtime
from domain import consumption, unit_rates

from . import serializers


def unit_rates(request):
    current_time = localtime.now()
    current_date = localtime.date(current_time)
    unit_rates_list = unit_rates.get_unit_rates_on_date(current_date)
    serializer = serializers.UnitRateSerializer(instance=unit_rates_list, many=True)
    unit_rates_json = json.dumps(serializer.data)

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


def home_consumption(request):
    date_list = consumption.get_consumption_available_dates()
    selected_date = localtime.parse_date(request.GET.get("date", date_list[0]))
    previous_date, next_date = consumption.get_previous_and_next_dates(date_list, selected_date)

    consumption_on_date = consumption.get_consumption_on_date(selected_date)
    usage_on_date = consumption.get_usage_on_date(consumption_on_date)
    payable_on_date = consumption.get_payable_on_date(consumption_on_date)

    return render(
        request,
        "dashboard/consumption.html",
        context={
            "usage_on_date": usage_on_date,
            "payable_on_date": payable_on_date,
            # TODO: use a serializer for this
            "consumption_json": json.dumps(consumption_on_date, cls=DjangoJSONEncoder),
            "selected_date": selected_date.isoformat(),
            "next_date": next_date,
            "previous_date": previous_date,
        },
    )

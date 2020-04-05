import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from . import consumption_helpers, helpers, serializers


def unit_rates(request):
    current_time = helpers.now()
    current_date = helpers.date(current_time)
    unit_rates_list = consumption_helpers.get_unit_rates(current_date)
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


def consumption(request):
    date_list = consumption_helpers.get_consumption_available_dates()
    selected_date = helpers.parse_date(request.GET.get("date", date_list[0]))
    previous_date, next_date = consumption_helpers.get_previous_and_next_dates(
        date_list, selected_date
    )

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

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from core import localtime
from domain import consumption, unit_rates

from . import serializers


def unit_rates_dashboard(request):
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


def consumption_dashboard(request):
    date_list = consumption.get_consumption_available_dates()
    selected_date = localtime.parse_date(request.GET.get("date", date_list[0]))
    previous_date, next_date = localtime.get_previous_and_next_dates(date_list, selected_date)

    elec_consumption_on_date = consumption.get_elec_consumption_on_date(selected_date)
    gas_consumption_on_date = consumption.get_gas_consumption_on_date(selected_date)
    elec_usage_on_date = consumption.get_usage_on_date(elec_consumption_on_date)
    gas_usage_on_date = consumption.get_usage_on_date(gas_consumption_on_date)
    payable_on_date = consumption.get_payable_on_date(elec_consumption_on_date + gas_consumption_on_date)

    return render(
        request,
        "dashboard/consumption.html",
        context={
            "elec_usage_on_date": elec_usage_on_date,
            "gas_usage_on_date": gas_usage_on_date,
            "payable_on_date": payable_on_date,
            # TODO: use a serializer for this
            "elec_consumption_json": json.dumps(elec_consumption_on_date, cls=DjangoJSONEncoder),
            "gas_consumption_json": json.dumps(gas_consumption_on_date, cls=DjangoJSONEncoder),
            # TODO: populate from somewhere else
            "gas_unit_rate": consumption.GAS_UNIT_RATE,
            "gas_standing_charge": consumption.GAS_STANDING_CHARGE,
            "selected_date": selected_date.isoformat(),
            "next_date": next_date,
            "previous_date": previous_date,
        },
    )

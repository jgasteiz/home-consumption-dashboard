from django.shortcuts import render

from data import models

from . import helpers


def home(request):
    date = helpers.parse_date(request.GET.get("date", helpers.yesterday().isoformat()))
    consumption_list = models.Consumption.objects.filter(
        interval_start__gte=helpers.midnight(date),
        interval_end__lte=helpers.next_midnight(date),
    )
    return render(
        request,
        "dashboard/dashboard.html",
        context={"consumption_list": consumption_list},
    )

from django.shortcuts import render

from data import models


def home(request):
    return render(
        request,
        "dashboard/dashboard.html",
        context={"consumption_list": models.Consumption.objects.all()},
    )

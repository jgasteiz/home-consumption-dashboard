from django.contrib import admin

from . import models


@admin.register(models.Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ("consumption", "interval_start", "interval_end")

from django.db import models


class Consumption(models.Model):
    consumption = models.DecimalField(decimal_places=4, max_digits=10)
    interval_start = models.DateTimeField()
    interval_end = models.DateTimeField()

    def __str__(self):
        start_time = self.interval_start.strftime("%H:%M")
        end_time = self.interval_end.strftime("%H:%M")
        return f"{self.interval_start.date()}: From {start_time} to {end_time}: {self.consumption}"

    class Meta:
        ordering = ["-interval_end"]


class UnitRate(models.Model):
    value_exc_vat = models.DecimalField(decimal_places=4, max_digits=10)
    value_inc_vat = models.DecimalField(decimal_places=4, max_digits=10)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        start_time = self.valid_from.strftime("%H:%M")
        end_time = self.valid_to.strftime("%H:%M")
        return (
            f"{self.valid_from.date()}: From {start_time} to {end_time}: £{self.value_inc_vat} "
            f"(£{self.value_exc_vat} exc VAT)"
        )

    class Meta:
        ordering = ["-valid_to"]

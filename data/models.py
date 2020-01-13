from django.db import models


class Consumption(models.Model):
    consumption = models.DecimalField(decimal_places=4, max_digits=10)
    interval_start = models.DateTimeField()
    interval_end = models.DateTimeField()

    class Meta:
        ordering = ["-interval_end"]

    def __str__(self):
        start_time = self.interval_start.strftime("%H:%M")
        end_time = self.interval_end.strftime("%H:%M")
        return f"{self.interval_start.date()}: From {start_time} to {end_time}: {self.consumption}"

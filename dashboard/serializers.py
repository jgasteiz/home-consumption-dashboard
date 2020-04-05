from rest_framework import serializers

from data import models


class UnitRateSerializer(serializers.ModelSerializer):
    valid_from = serializers.DateTimeField(format="%H:%M")
    valid_to = serializers.DateTimeField(format="%H:%M")

    class Meta:
        model = models.UnitRate
        fields = (
            "value_exc_vat",
            "value_inc_vat",
            "valid_from",
            "valid_to",
        )

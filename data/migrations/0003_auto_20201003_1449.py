# Generated by Django 3.0.3 on 2020-10-03 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_auto_20200405_0938"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Consumption", new_name="ElectricityConsumption",
        ),
    ]

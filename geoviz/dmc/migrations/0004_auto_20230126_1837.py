# Generated by Django 3.2 on 2023-01-26 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0003_auto_20230126_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ddc_upload',
            name='flight_mission_guid',
        ),
        migrations.RemoveField(
            model_name='ddc_upload',
            name='mosaiced_image',
        ),
        migrations.RemoveField(
            model_name='historicalddc_upload',
            name='flight_mission_guid',
        ),
        migrations.RemoveField(
            model_name='historicalddc_upload',
            name='mosaiced_image',
        ),
    ]
# Generated by Django 3.2 on 2023-01-27 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0010_auto_20230127_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddc_upload',
            name='flight_mission_guid',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Dronelogbook Id'),
        ),
        migrations.AlterField(
            model_name='historicalddc_upload',
            name='flight_mission_guid',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Dronelogbook Id'),
        ),
    ]

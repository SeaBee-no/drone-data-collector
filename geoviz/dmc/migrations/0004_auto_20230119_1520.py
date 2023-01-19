# Generated by Django 3.2 on 2023-01-19 14:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0003_auto_20230119_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddc_main',
            name='drone_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=300, verbose_name='Drone Type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalddc_main',
            name='drone_type',
            field=models.CharField(default=datetime.datetime(2023, 1, 19, 14, 20, 31, 355688, tzinfo=utc), max_length=300, verbose_name='Drone Type'),
            preserve_default=False,
        ),
    ]

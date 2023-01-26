# Generated by Django 3.2 on 2023-01-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0006_auto_20230126_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ddc_upload',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='historicalddc_upload',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='ddc_upload',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalddc_upload',
            name='id',
            field=models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID'),
        ),
    ]
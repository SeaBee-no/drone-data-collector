# Generated by Django 3.2 on 2023-01-26 17:05

from django.db import migrations, models
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddc_upload',
            name='mosaiced_image',
            field=models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='dmc'), upload_to=django_minio_backend.models.iso_date_prefix, verbose_name='Upload single mosaiced file'),
        ),
        migrations.AddField(
            model_name='historicalddc_upload',
            name='mosaiced_image',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload single mosaiced file'),
        ),
    ]
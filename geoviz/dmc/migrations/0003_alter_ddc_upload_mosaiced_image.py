# Generated by Django 3.2 on 2023-02-15 12:18

from django.db import migrations, models
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0002_alter_ddc_upload_mosaiced_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddc_upload',
            name='mosaiced_image',
            field=models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='geoviz-upload-data'), upload_to='<function iso_date_prefix at 0x000002197078C670>/deb', verbose_name='Upload single mosaiced file'),
        ),
    ]

# Generated by Django 3.2 on 2023-02-17 12:36

from django.db import migrations, models
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('dmc', '0007_alter_ddc_upload_mosaiced_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddc_upload',
            name='mosaiced_image',
            field=models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='geoviz-upload-data'), upload_to='2023/deb/', verbose_name='Upload single mosaiced file'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-04-27 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0025_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abcpethost',
            name='album_host_image',
            field=models.FileField(blank=True, null=True, upload_to='album_host_images'),
        ),
    ]

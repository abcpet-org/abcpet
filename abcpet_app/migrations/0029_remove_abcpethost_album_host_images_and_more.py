# Generated by Django 5.0.1 on 2024-04-28 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0028_remove_abcpethost_album_host_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abcpethost',
            name='album_host_images',
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='album_host_images',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_album_host'),
        ),
    ]

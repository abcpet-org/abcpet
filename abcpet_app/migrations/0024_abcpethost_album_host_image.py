# Generated by Django 5.0.1 on 2024-04-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0023_remove_abcpethost_verificado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='abcpethost',
            name='album_host_image',
            field=models.ImageField(blank=True, null=True, upload_to='album_host_images/'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-01-02 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0006_userprofile_fecha_nacimiento_userprofile_genero_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='state',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='calle_numero',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Calle y Número'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='comuna',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Comuna'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='info_adicional',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Información Adicional'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='region',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Región'),
        ),
    ]

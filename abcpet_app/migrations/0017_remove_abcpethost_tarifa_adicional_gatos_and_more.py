# Generated by Django 4.2.7 on 2024-01-16 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0016_abcpethost_comuna_host_abcpethost_direccion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abcpethost',
            name='tarifa_adicional_gatos',
        ),
        migrations.RemoveField(
            model_name='abcpethost',
            name='tarifa_adicional_perros',
        ),
        migrations.RemoveField(
            model_name='abcpethost',
            name='tarifa_estancia_prolongada',
        ),
        migrations.RemoveField(
            model_name='abcpethost',
            name='tarifa_hospedaje',
        ),
        migrations.RemoveField(
            model_name='abcpethost',
            name='tarifa_vacaciones',
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='servicio_en_casa_mascota',
            field=models.BooleanField(default=False, verbose_name='En casa de la mascota'),
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='servicio_guarderia',
            field=models.BooleanField(default=False, verbose_name='Guardería'),
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='servicio_hotel',
            field=models.BooleanField(default=False, verbose_name='Hotel'),
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='servicio_paseo_mascota',
            field=models.BooleanField(default=False, verbose_name='Paseo mascota'),
        ),
        migrations.AddField(
            model_name='abcpethost',
            name='tarifa_hotel',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Hotel'),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='region',
            field=models.CharField(choices=[('Metropolitana', 'Metropolitana')], default='Metropolitana', max_length=100),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='tarifa_aseo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Aseo'),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='tarifa_cuidado_casa',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Cuidado en Casa'),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='tarifa_guarderia',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Guardería'),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='tarifa_paseo_perros',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Paseo Perros'),
        ),
        migrations.AlterField(
            model_name='abcpethost',
            name='tarifa_recogida_entrega',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tarifa Recogida y Entrega'),
        ),
    ]

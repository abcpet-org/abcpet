# Generated by Django 5.2 on 2025-05-08 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abcpet_app', '0034_otpcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otpcode',
            options={'ordering': ['-created_at']},
        ),
    ]

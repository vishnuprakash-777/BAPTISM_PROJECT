# Generated by Django 5.1.4 on 2025-01-15 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0039_certificate_qr_code_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='qr_code_url',
        ),
    ]

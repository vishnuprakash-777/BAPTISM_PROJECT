# Generated by Django 5.1.4 on 2025-01-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0040_remove_certificate_qr_code_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='qr_code_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

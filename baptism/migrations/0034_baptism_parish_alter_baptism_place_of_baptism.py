# Generated by Django 5.1.3 on 2024-12-28 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0033_baptism_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='baptism',
            name='parish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='baptism.parishdetails'),
        ),
        migrations.AlterField(
            model_name='baptism',
            name='place_of_baptism',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

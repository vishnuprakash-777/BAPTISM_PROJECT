# Generated by Django 5.1.3 on 2024-12-28 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0030_alter_option_q_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='q_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='baptism.question'),
        ),
    ]

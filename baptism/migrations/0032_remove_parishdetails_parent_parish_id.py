# Generated by Django 5.1.3 on 2024-12-28 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baptism', '0031_alter_option_q_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parishdetails',
            name='parent_parish_id',
        ),
    ]

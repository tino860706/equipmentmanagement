# Generated by Django 3.1.4 on 2022-02-19 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220219_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentissue',
            old_name='is_issue',
            new_name='is_issued',
        ),
    ]

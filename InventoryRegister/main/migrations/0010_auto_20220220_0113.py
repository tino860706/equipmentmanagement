# Generated by Django 3.1.4 on 2022-02-19 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20220219_2345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentissue',
            old_name='issued_with',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='equipmentissuetag',
            old_name='issued_with',
            new_name='slug',
        ),
    ]

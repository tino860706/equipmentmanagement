# Generated by Django 3.1.4 on 2022-04-10 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_equipmentissue_row'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentissue',
            name='row',
        ),
    ]
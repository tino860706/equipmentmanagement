# Generated by Django 3.1.4 on 2022-02-19 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220219_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentissue',
            name='slug',
            field=models.SlugField(max_length=48),
        ),
    ]
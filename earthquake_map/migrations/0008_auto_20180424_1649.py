# Generated by Django 2.0.4 on 2018-04-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earthquake_map', '0007_earthquake_object_public_exists'),
    ]

    operations = [
        migrations.AddField(
            model_name='earthquake_object',
            name='closest_city',
            field=models.CharField(default='false', max_length=400),
        ),
        migrations.AddField(
            model_name='earthquake_object',
            name='distance',
            field=models.CharField(default='false', max_length=200),
        ),
    ]

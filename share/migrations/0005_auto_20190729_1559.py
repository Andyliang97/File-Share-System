# Generated by Django 2.2.3 on 2019-07-29 19:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0004_videoinfo_aws_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoinfo',
            name='movie_name',
            field=models.CharField(default='', max_length=256, verbose_name='Movie name'),
        ),
        migrations.AddField(
            model_name='videoinfo',
            name='overview',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='videoinfo',
            name='rating',
            field=models.CharField(default='0.0', max_length=8, verbose_name='Rating'),
        ),
        migrations.AddField(
            model_name='videoinfo',
            name='release_date',
            field=models.DateField(default=datetime.date(2019, 7, 29), verbose_name='Release date'),
        ),
    ]

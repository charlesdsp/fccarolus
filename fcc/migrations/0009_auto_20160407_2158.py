# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0008_auto_20160407_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='/avatar/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tel',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

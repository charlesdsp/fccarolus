# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0002_auto_20160403_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='dateMatch',
            field=models.DateField(null=True),
        ),
    ]

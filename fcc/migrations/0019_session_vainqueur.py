# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0018_notematch'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='vainqueur',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]

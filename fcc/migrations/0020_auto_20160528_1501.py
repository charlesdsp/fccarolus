# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0019_session_vainqueur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='ouverte',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0011_auto_20160409_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfcc',
            name='dtUpdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
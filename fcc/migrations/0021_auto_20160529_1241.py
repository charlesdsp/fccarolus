# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-29 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0020_auto_20160528_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='scoreA',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='scoreB',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0013_award_awardvainqueur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfcc',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
    ]

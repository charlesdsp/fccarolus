# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 17:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0010_auto_20160409_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfcc',
            old_name='iduserFCC',
            new_name='idUserFCC',
        ),
        migrations.AddField(
            model_name='userfcc',
            name='dtUpdate',
            field=models.DateField(auto_now=True, default=datetime.datetime(2016, 4, 9, 17, 24, 35, 874778, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

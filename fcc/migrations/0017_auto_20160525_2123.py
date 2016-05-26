# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-25 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0016_joker'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultat',
            name='moyenne_note',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='resultat',
            name='somme_notes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userfcc',
            name='has_voted',
            field=models.BooleanField(default=False),
        ),
    ]

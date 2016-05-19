# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0007_auto_20160404_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compo',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Session'),
        ),
        migrations.AlterField(
            model_name='compo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.User'),
        ),
        migrations.AlterField(
            model_name='match',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Session'),
        ),
        migrations.AlterField(
            model_name='resultats',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Match'),
        ),
        migrations.AlterField(
            model_name='resultats',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.User'),
        ),
        migrations.AlterField(
            model_name='stats',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Session'),
        ),
        migrations.AlterField(
            model_name='stats',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.User'),
        ),
    ]

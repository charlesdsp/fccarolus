# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id_match', models.AutoField(primary_key=True, serialize=False)),
                ('ouverte', models.BooleanField(default=False)),
                ('inscrits', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id_session', models.AutoField(primary_key=True, serialize=False)),
                ('nombreMatchs', models.IntegerField(default=0)),
                ('ouverte', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Session'),
        ),
    ]
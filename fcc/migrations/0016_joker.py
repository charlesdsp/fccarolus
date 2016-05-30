# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 21:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcc', '0015_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Joker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joker', models.CharField(max_length=20)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.Match')),
                ('userFCC', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcc.UserFCC')),
            ],
        ),
    ]
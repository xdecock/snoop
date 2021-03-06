# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-26 21:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snoop', '0007_auto_20161026_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='slug',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snoop.Collection'),
        ),
    ]

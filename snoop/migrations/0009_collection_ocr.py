# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 19:11
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snoop', '0008_auto_20161026_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='ocr',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maldini', '0028_auto_20160621_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='sha1',
            field=models.CharField(blank=True, db_index=True, default='', max_length=50),
            preserve_default=False,
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maldini', '0036_auto_20160629_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('md5', models.CharField(db_index=True, max_length=40)),
                ('path', models.CharField(max_length=4000)),
                ('text', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ocr',
            unique_together=set([('tag', 'md5')]),
        ),
    ]
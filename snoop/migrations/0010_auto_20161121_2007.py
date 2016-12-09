# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 20:07
from __future__ import unicode_literals

from pathlib import Path
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def generate_default_ocr_sets(apps, schema_editor):
    Ocr = apps.get_model('snoop', 'Ocr')
    Collection = apps.get_model('snoop', 'Collection')
    Document = apps.get_model('snoop', 'Document')

    if not Ocr.objects.exists():
        return

    if not hasattr(settings, 'SNOOP_OCR_ROOT'):
        raise RuntimeError("SNOOP_OCR_ROOT is not set in the django config")
    old_root = Path(settings.SNOOP_OCR_ROOT)

    default_collection = (
        Collection.objects
        .order_by('id')
        .first()
    )
    if not default_collection:
        raise RuntimeError("There are OCR objects but no Collection object!")

    tags = {ocr.tag for ocr in Ocr.objects.distinct('tag')}
    for tag in tags:
        ocrDocument = Ocr.objects.filter(tag=tag).first()
        try:
            document = (
                Document.objects
                .filter(md5=ocrDocument.md5)
                .first()
            )
            collection = document.collection
        except Document.NotFound:
            collection = default_collection
        collection.ocr[tag] = str(old_root / tag)
        collection.save()
        Ocr.objects.filter(tag=tag).update(collection=collection)
    Ocr.objects.filter(collection_id__isnull=True).update(collection_id=default_collection.id)

def do_nothing(*args):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('snoop', '0009_collection_ocr'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocr',
            name='collection',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_documents',
                to='snoop.Collection'),
        ),
        migrations.RunPython(generate_default_ocr_sets, do_nothing),
        migrations.AlterField(
            model_name='ocr',
            name='collection',
            field=models.ForeignKey(
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_documents',
                to='snoop.Collection'),
        ),
        migrations.AlterUniqueTogether(
            name='ocr',
            unique_together=set([('collection', 'tag', 'md5')]),
        ),
    ]

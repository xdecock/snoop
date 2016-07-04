from pathlib import Path
from dateutil import parser
from pprint import pformat
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.utils.encoding import filepath_to_uri
from jinja2 import Environment
from . import models
from .digest import digest
from .walker import files_in
BOOTSTRP_CSS = ""

path = Path(settings.BASE_DIR) / 'assets' / 'bootstrap.min.css'
with path.open('r') as f:
    BOOTSTRP_CSS += f.read() + "\n"

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'css': BOOTSTRP_CSS,
        'uriencode': filepath_to_uri,
    })
    return env

def _format_size(num):
    for unit in ['', 'KB', 'MB', 'GB', 'TB']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%3.1f %s" % (num, 'PB')

def _format_date(date_value):
    return parser.parse(date_value).strftime("%d %B %Y")

def document_raw(request, id):
    doc = get_object_or_404(models.Document, id=id)
    if doc.content_type == 'text/html':
        return HttpResponse("Not serving HTML files, they can be dangerous")
    with doc.open() as f:
        data = f.read()
        return HttpResponse(data, content_type=doc.content_type)

def document_ocr(request, id, tag):
    doc = get_object_or_404(models.Document, id=id)
    ocr = get_object_or_404(models.Ocr, tag=tag, md5=doc.md5)
    return FileResponse(
        ocr.absolute_path.open('rb'),
        content_type='application/pdf',
    )

def doc_children(doc):
    children = models.Document.objects.filter(container=doc)
    return [{
                'id': child.id,
                'filename': child.filename,
                'size': child.disk_size,
                'content_type': child.content_type,
            } for child in children]

def document(request, id):
    up = None
    attachments = []

    if id == '0':
        data = {
            'type': 'folder',
            'files': files_in(''),
        }
        ocr_tags = []

    else:
        doc = get_object_or_404(models.Document, id=id)

        try:
            data = digest(doc)

        except:
            data = {'type': '-- ERROR --'}

        else:
            if data.get('type') == 'folder':
                data['files'] = files_in(doc.path + '/')
            elif data.get('type') == 'archive':
                data['files'] = doc_children(doc)

            if 'files' in data:
                for file in data['files']:
                    file['size'] = _format_size(file['size'])

            def attachment_id(n):
                try:
                    a = doc.document_set.get(path=n)
                except models.Document.DoesNotExist:
                    return None
                else:
                    return a.id

            if data.get('tree'):
                data['tree'] = pformat(data.get('tree'), indent=4, width=120)

            attachments = [{
                'filename': a['filename'],
                'id': attachment_id(n),
                'content_type': a['content_type'],
            } for n, a in data.get('attachments', {}).items()]

            if doc.container:
                up = doc.container.id
            elif '/' in doc.path:
                up_path = doc.path.rsplit('/', 1)[0]
                up = (
                    models.Document.objects
                    .get(container=None, path=up_path)
                    .id
                )
            else:
                up = 0

    for field in ['date', 'date-created']:
        if data.get(field):
            data[field] = _format_date(data[field])

    return render(request, 'document.html', {
        'id': id,
        'up': up,
        'data': data,
        'attachments': attachments,
    })

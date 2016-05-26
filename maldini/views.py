from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Document
from .digest import digest

def document(request, id):
    doc = get_object_or_404(Document, id=id)
    data = digest(doc)
    return render(request, 'document.html', {
        'data': data,
    })

from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(settings.ELASTICSEARCH_URL)

MAPPINGS = {
    "doc": {
        "properties": {
            "id": {"type": "string", "index": "not_analyzed"},
            "path": {"type": "string", "index": "not_analyzed"},
            "suffix": {"type": "string", "index": "not_analyzed"},
            "md5": {"type": "string", "index": "not_analyzed"},
            "sha1": {"type": "string", "index": "not_analyzed"},
            "filetype": {"type": "string", "index": "not_analyzed"},
            "lang": {"type": "string", "index": "not_analyzed"},
            "date": {"type": "date", "index": "not_analyzed"},
            "date_created": {"type": "date", "index": "not_analyzed"},
        }
    }
}


class Command(BaseCommand):
    help = "Reset the elasticsearch index"

    def handle(self, **options):
        es.indices.delete(settings.ELASTICSEARCH_INDEX, ignore=[400, 404])
        es.indices.create(settings.ELASTICSEARCH_INDEX, {
            "mappings": MAPPINGS,
        })

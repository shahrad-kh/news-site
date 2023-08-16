from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import News


@registry.register_document
class NewsDocument(Document):
    """
    document class that represent the Elasticsearch documents and 
    their mappings
    """
    
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField()
        }
    )
    content = fields.TextField(
        attr='content',
        fields={
            'raw': fields.TextField()
        }
    )
    tags = fields.TextField(
        attr='tags_indexing',
        fields={
            'raw': fields.TextField(multi=True)
        },
        multi=True
    )
    source = fields.TextField(
        attr='source',
        fields={
            'raw': fields.TextField()
        }
    )
    
    class Index:
        name = 'news'
       
    
    class Django:
        model = News
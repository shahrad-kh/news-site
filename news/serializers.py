from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import NewsDocument
from .models import News, Tag


class NewsSerializer(serializers.ModelSerializer):
    """
    Serializer for News model
    """
    
    # To use Tag.__str__ for serialization
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'tags', 'source']


class NewsDocumentSerializer(DocumentSerializer):
    """
    Serializer for NewsDocument
    """
    
    class Meta:
        document = NewsDocument
        fields = ['id', 'title', 'content', 'tags', 'source']
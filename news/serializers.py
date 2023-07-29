from rest_framework import serializers

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
        
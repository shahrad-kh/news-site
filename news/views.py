from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .documents import NewsDocument
from .models import News
from .serializers import NewsSerializer


class NewsListAPI(ListAPIView):
    """
    Displays news list 
    """
    
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filterset_fields = ['tags', 'tags__title']
    

class NewsDetailRetrieveAPI(RetrieveAPIView):
    """
    Displays news details by news id
    """
    
    queryset  = News.objects.all()
    serializer_class = NewsSerializer


class NewsDocumentView(DocumentViewSet):
    """
    Display news and provide search within news using elastic search like this:
        .../api/news-search?search={value} or {terms}
    """
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    
    filter_backends = [
    	SearchFilterBackend
    ]
    
    search_fields = ['title', 'content', 'tags']
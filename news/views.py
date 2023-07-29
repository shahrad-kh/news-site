from rest_framework.generics import ListAPIView, RetrieveAPIView

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
    
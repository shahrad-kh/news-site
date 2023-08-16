from django.urls import path
from rest_framework import routers

from . import views


app_name = 'news'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'news-search', views.NewsDocumentView, basename='News-search')

urlpatterns = [
    path('news/', views.NewsListAPI.as_view(), name="news_page"),
    path('news/<int:pk>/', views.NewsDetailRetrieveAPI.as_view(), name="detail_page_by_pk"),
]
urlpatterns += router.urls

# To delete additional urls
urlpatterns = [url for url in urlpatterns if not str(url.pattern).startswith('^news-search/')]

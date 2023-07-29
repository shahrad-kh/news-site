from django.urls import path

from . import views


app_name = 'news'

urlpatterns = [
    path('news/', views.NewsListAPI.as_view(), name="news_page"),
    path('news/<int:pk>/', views.NewsDetailRetrieveAPI.as_view(), name="detail_page_by_pk"),
]

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# from news.models import News, Tag
from news.models import News, Tag

def create_news_for_test():
    """
    Create two instance of class Tag and then create a news for test class

    Returns:
        dict: dict type of the news
    """

    tag1 = Tag.objects.create(title='tag1')
    tag2 = Tag.objects.create(title='tag2')
    news = News.objects.create(
        title = 'test_news',
        content = 'test_news_content',
        source = 'test_news_source'
    )
    news.tags.set([tag1, tag2])
    
    # Convert instance to dict
    news_dict = {
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'tags': [tag1.title, tag2.title],
        'source': news.source,
    }
    
    return news_dict


class NewsListTest(TestCase):
    """
    To test news page functionality
    """
    
    def setUp(self):
        self.client = APIClient()
        self.news = create_news_for_test()
        
    
    def test_news_list(self):
        url = reverse("news:news_page")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), News.objects.count())
        
        # Checks the equality of test_news and last news
        self.assertEqual(self.news, dict(response.data[-1]))
        
    
    def test_news_detail(self):
        url = reverse("news:detail_page_by_pk", kwargs={'pk': self.news['id']})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(self.news))
        
        # Checks the equality of test_news id and object in response data
        self.assertEqual(self.news['id'], dict(response.data)['id'])

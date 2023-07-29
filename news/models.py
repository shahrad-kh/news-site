from django.db import models


class Tag(models.Model):
    """
    Model to create tags for news
    """
    
    title = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.title
    
    
class News(models.Model):
    """
    Model to store news
    """

    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    source = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
        
    
    def __str__(self):
        return self.title
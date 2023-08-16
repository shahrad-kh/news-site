from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry


@receiver(post_save)
def update_document(sender, **kwargs):
    """
    To update created database instances in elastic database
    """
    
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']
    
    if app_label == 'news':
        if model_name == 'News':
            instances = instance.News.all()
            for _instance in instances:
                registry.update(_instance)
                

@receiver(post_delete)
def delete_document(sender, **kwargs):
    """
    To update deleted database instances in elastic database
    """
    
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'news':
        if model_name == 'News':
            instances = instance.article.all()
            for _instance in instances:
                registry.update(_instance)
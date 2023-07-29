from django.contrib import admin

from .models import News, Tag


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source']


admin.site.register(Tag)
admin.site.register(News, NewsAdmin)

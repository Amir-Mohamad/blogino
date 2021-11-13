from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class ArticleService():
    serializer_class = ArticleSerializer

    def get_all_article(self, request):
        """use to find all articles (using catch)"""
        articles = Article.objects.all()
        if 'api_articles' in cache:
            serializer = cache.get('api_articles')
            return serializer

        serializer = self.serializer_class(articles, many=True)
        cache.set('api_articles', serializer, timeout=CACHE_TTL)

        return serializer

    def get_single_article(self, request, article_id):
        """use to find single article from article_id (using catch)"""

        article = get_object_or_404(Article, pk=article_id)
        if 'api_article' in cache:
            serializer = cache.get('api_article')
            return serializer
        
        serializer = self.serializer_class(article)
        cache.set('api_article', serializer, timeout=CACHE_TTL)

        return serializer





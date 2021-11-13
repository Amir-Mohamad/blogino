from django.shortcuts import get_object_or_404
from .models import Article, Category
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ArticleListView(APIView):
    serializer_class = ArticleSerializer

    def get(self, request):
        articles = Article.objects.all()
        if 'articles' in cache:
            data = cache.get('articles')
            return Response(data.data, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(articles, many=True)
        cache.set('articles', serializer, timeout=CACHE_TTL)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    serializer_class = ArticleSerializer

    def get(self,request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        if 'article' in cache:
            data = cache.get('article')
            return Response(data.data, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(article)
        cache.set('article', serializer, timeout=CACHE_TTL)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import get_object_or_404

from .services import ArticleService
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
    service = ArticleService()

    def get(self, request):
        serializer = self.service.get_all_article(request=request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    service = ArticleService()

    def get(self,request, article_id):
        data = self.service.get_single_article(request=request, article_id=article_id)
        return Response(data.data, status=status.HTTP_200_OK)


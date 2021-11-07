from .models import Article, Category
from rest_framework.generics import ListAPIView
from .serializers import ArticleListSerializer


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
from rest_framework import serializers
from .models import Article, Category


class ArticleListSerializer(serializers.ModelSerializer):
    article_likes_count = serializers.ReadOnlyField(source="likes_count")
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
         return obj.author.first_name or obj.author.email


    class Meta:
        model = Article
        fields = (
            'id',
            'author',
            'title',
            'slug',
            'content',
            'image',
            'created',
            'updated',
            'status',
            'article_likes_count'
        )
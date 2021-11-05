from celery import Celery
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Article
from config.celery import celery_app


User = get_user_model()


@celery_app.task
def task_like_article(article_id, user_id):
    """
        Let user to like an article 👇
    """
    user = get_object_or_404(User, pk=user_id)
    article = get_object_or_404(Article, id=article_id)
    if article.likes.filter(id=user_id).exists():
        article.likes.remove(user)

    else:
        article.likes.add(user)

    return

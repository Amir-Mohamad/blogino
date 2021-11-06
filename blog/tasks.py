from celery import Celery
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Article, Comment
from config.celery import celery_app
from django.core.mail import send_mail
from django.conf import settings


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

@celery_app.task
def task_send_mail(user_id, comment_id, user_replied_id):
    user = get_object_or_404(User, pk=user_id)
    comment = get_object_or_404(Comment, id=comment_id)
    user_replied = get_object_or_404(User, pk=user_replied_id)
    msg = f'{user} add reply on your comment: "{comment.body[:20]}"'
    subject = 'reply'
    print(user_replied, '*'*80)
    send_mail(subject, msg, settings.EMAIL_HOST_USER, ('y.amirmohamad8413@gmail.com',))
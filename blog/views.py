from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import get_user_model
from .models import Article
from .tasks import task_like_article
from .mixins import CacheMixin
User = get_user_model()
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def home(request):
    articles = Article.objects.all()
    if 'articles' in cache:
        data = cache.get('articles')
        return render(request, 'blog/home.html', {
            'object_list': data,
        })
    cache.set('articles', articles,timeout=CACHE_TTL)
    return render(request, 'blog/home.html', {
        'object_list': articles,
    })


class ArticleDetailView(View):
    template_name = 'blog/article_detail.html'

    def get(self,request, pk):
        article = get_object_or_404(Article, pk=pk)
        if 'article' in cache:
            data = cache.get('article')
            return render(request, self.template_name, {
            'obj': data,
          })
        cache.set('article', article, timeout=CACHE_TTL)
        return render(request, self.template_name, {
            'obj': article,
        })

class BlogLike(View):

    def get(self, request, article_id):
        # If i pass the request into task, then i will have too many bugs
        user = User.objects.get(id=request.user.id)
        user_id = user.id
        task_like_article.delay(user_id=user_id, article_id=article_id)

        return redirect('blog:detail', article_id)

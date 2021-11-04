from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import get_user_model
from .models import Article
from .tasks import task_like_article

User = get_user_model()


class HomePage(ListView):
    model = Article
    template_name = 'blog/home.html'


class ArticleDetailView(DetailView):
    model = Article


class BlogLike(View):

    def get(self, request, article_id):
        # If i pass the request into task, then i will have too many bugs
        user = User.objects.get(id=request.user.id)
        user_id = user.id
        task_like_article.delay(user_id=user_id, article_id=article_id)

        return redirect('blog:home')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import get_user_model
from .models import Article, Comment
from .tasks import task_like_article
from .mixins import CacheMixin
from .forms import AddCommentForm, AddReplyForm
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

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


# class ArticleDetailView(View):
#     template_name = 'blog/article_detail.html'
#     comment_form_class = CommentForm
#     reply_form_class = ReplyForm

#     def get(self, request, pk):
#         article = get_object_or_404(Article, pk=pk)
#         if 'article' in cache:
#             data = cache.get('article')
#             return render(request, self.template_name, {
#             'obj': data,
#           })
#         cache.set('article', article, timeout=CACHE_TTL)
#         return render(request, self.template_name, {
#             'obj': article,
#         })
#     def post(self, request):


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article, is_reply=False)
    reply_form = AddReplyForm()
    # if request.user.is_authenticated:
    # 	if article.user_can_like(request.user):
    # 		can_like = True
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'you comment submitted successfully')
    else:
        form = AddCommentForm()
    return render(request, 'blog/article_detail.html', {
        'article':article,
        'comments':comments,
        'form':form,
        'reply':reply_form,
        })

@login_required
def add_reply(request, article_id, comment_id):
    article = get_object_or_404(Article, pk=article_id)
    print(article)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.article = article
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted successfully', 'success')
    return redirect('blog:detail', article.pk)




class BlogLike(View):

    def get(self, request, article_id):
        # If i pass the request into task, then i will have too many bugs
        user = User.objects.get(id=request.user.id)
        user_id = user.id
        task_like_article.delay(user_id=user_id, article_id=article_id)

        return redirect('blog:detail', article_id)

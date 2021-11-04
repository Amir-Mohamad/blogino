from django.urls import path


from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<pk>/', views.ArticleDetailView.as_view(), name='detail'),

    # likes
    path('like/article/<int:article_id>/',
         views.BlogLike.as_view(), name='like'),

]

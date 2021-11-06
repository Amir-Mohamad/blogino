from django.urls import path


from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<pk>/', views.article_detail, name='detail'),
    path('add_reply/<int:article_id>/<int:comment_id>/', views.add_reply, name='add_reply'),


    # likes
    path('like/article/<int:article_id>/',
         views.BlogLike.as_view(), name='article_like'),

]

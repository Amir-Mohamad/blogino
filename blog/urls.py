from django.urls import path, include
from . import views
from . import api_views

api_urls = [
	path('article_list/', api_views.ArticleListView.as_view(), name='article_list')
]



app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<pk>/', views.article_detail, name='detail'),
    path('add_reply/<int:article_id>/<int:comment_id>/', views.add_reply, name='add_reply'),


    # likes
    path('like/article/<int:article_id>/',
         views.BlogLike.as_view(), name='article_like'),

    path('api/', include(api_urls))

]

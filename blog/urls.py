from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]

from django.shortcuts import render
from django.views.generic import ListView
from .models import Article


class HomePage(ListView):
    model = Article
    template_name = 'blog/home.html'

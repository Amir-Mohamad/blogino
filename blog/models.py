from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from blog.utils import slugify_instance_title

User = get_user_model()


class Category(models.Model):
    title = models.TextField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS = [
        ('D', 'Draft'),
        ('P', 'Publish'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog-images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250, choices=STATUS)
    likes = models.ManyToManyField(
        User, related_name='blog_like', null=True, blank=True)
    # def get_absolute_url(self):
    #     return reverse("blog:detail", kwargs={"id": self.id})

    def __str__(self):
        return self.title

    def likes_count(self=None, d=None):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if self.slug is None:
            slugify_instance_title(self, save=False)
        super(Article, self).save(*args, **kwargs)

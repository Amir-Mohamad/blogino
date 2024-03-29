from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from blog.utils import slugify_instance_title
from sorl.thumbnail import ImageField
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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    image = ImageField(upload_to='blog-images/') # using sorl-thumbnail
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


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='acomment')
	reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomment')
	is_reply = models.BooleanField(default=False)
	body = models.TextField(max_length=400)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} - {self.body[:30]}'

	class Meta:
		ordering = ('-created',)

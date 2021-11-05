from django.test import Client, TestCase
from django.urls import reverse
from ..models import Article, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='y.amirmohamad8413@gmail.com', password="amiramir1234")
        category = Category.objects.create(title='django')
        cls.article = Article.objects.create(title='title django', content="content", image="blog-images/1.jpg", status="P", author=user, category=category)


    def test_home_page_view(self):
        url = reverse("blog:home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
    
    def test_single_course(self):
        url = reverse('blog:detail', args=[self.article.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
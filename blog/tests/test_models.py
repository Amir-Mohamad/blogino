from blog.models import Article
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
User = get_user_model()


class ArticleModel(TestCase):
    """
    Things to test:
    - Can be create a article with the bare minimum of fields? (Title, content and author)
    - Does the __str__ method behave as expected?
    - Is a slug automatically created?
    - Do two articles with the same title and user get different slugs?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
            password='password456'
        )

        cls.article = Article.objects.create(
            title='My blog article',
            content='This is my first article',
            author=cls.user,
        )

    def article(self):
        """ Tests that a article with a title, content, user and creation date can be created"""

        self.assertEqual(self.article.title, 'My blog article')
        self.assertEqual(self.article.author, self.user)

    def article_str(self):
        """ Tests the __str__ of the article model"""

        self.assertEqual(str(self.article), 'My blog article | by user123')

    def test_creates_a_slug(self):
        """ Tests a slug is automatically created """

        self.assertEqual(self.article.slug, 'my-blog-article')

    def test_slugs_are_unique(self):
        """ Tests two articles with identical titles from the same author receive different slugs """

        second_title = Article.objects.create(
            title='My blog article',
            content='This is my second article',
            author=self.user,
        )

        self.assertNotEqual(self.article.slug, second_title.slug)

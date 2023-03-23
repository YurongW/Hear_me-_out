from django.test import TestCase
from Post.models import Category


# Create your tests here.
class IndexPageTest(TestCase):
    """test index"""

    def test_index_page(self):
        """test index view"""
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_popular_page(self):
        Category.objects.create(name="test")
        response = self.client.get('/popularpost/test/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

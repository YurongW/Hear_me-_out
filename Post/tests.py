import uuid

from django.test import TestCase
from Account.models import Account
from Post.models import Topic, Category, Comment
from Post.serializers import PullPostSerializer


# Create your tests here.
class PostAction(TestCase):
    def setUp(self) -> None:
        self.account = Account.objects.create(username="test", password="admin")
        self.category = Category.objects.create(name="test")
        self.topic = Topic.objects.create(name="test", category=self.category, customer_id=self.account, content="test",
                                          uuid=str(uuid.uuid4()))

    def test_upgrade_admin(self):
        self.account.is_superuser = True
        self.account.save()
        self.assertTrue(self.account.is_superuser)

    def test_read_post(self):
        self.assertEqual(Topic.objects.get(uuid=self.topic.uuid).content, self.topic.content)

    def test_PostSerializer(self):
        post = PullPostSerializer(data={"category": self.category.name, "topic": "test", "images": [], "content": "contentText"})
        self.assertTrue(post.is_valid())
        topic = post.save()
        self.assertEqual(Topic.objects.get(uuid=topic.uuid).content, "contentText")
from django.test import TestCase
from Account.models import Account


# Create your tests here.

class AccountTestCase(TestCase):
    def setUp(self) -> None:
        self.account = Account.objects.create(
            username="test_user",
            password="testtest",
            is_deleted=False,
        )

    def test_account_model(self):
        self.assertTrue(self.account.is_active)
        self.assertFalse(self.account.is_deleted)
        self.assertEqual(self.account.avatar, "/media/pic/default.jpg")
    
        self.account.num_post += 1
        self.account.num_like += 1
        self.account.save()
        self.assertEqual(self.account.num_post, 1)
        self.assertEqual(self.account.num_like, 1)

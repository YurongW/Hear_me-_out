from django.db import models

from Account.models import Account


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=256, verbose_name="topic name")
    like = models.IntegerField(default=0)
    customer_id = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="customers", null=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    uuid = models.UUIDField()
    num_comment = models.IntegerField(default=0)


class TopicPicture(models.Model):
    url = models.URLField()
    topic_id = models.ForeignKey(to=Topic, on_delete=models.CASCADE)


class Comment(models.Model):
    customer_id = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="customers_comment", null=True)
    topic_id = models.ForeignKey(to=Topic, on_delete=models.CASCADE, related_name="customers_comment", null=True)
    content = models.TextField()
    num_like = models.IntegerField(default=0)
    uuid = models.UUIDField()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="category name", unique=True)
    num_post = models.IntegerField(default=0)
    num_like = models.IntegerField(default=0)


class RecordLike(models.Model):
    uuid = models.UUIDField(verbose_name="record uuid")
    customer_id = models.IntegerField(verbose_name="record customer_id")

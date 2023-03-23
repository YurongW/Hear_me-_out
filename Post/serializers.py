import uuid

from rest_framework import serializers
from rest_framework.exceptions import APIException

from Post.models import Topic, Category, Comment, TopicPicture


class CategoryNotFoundError(APIException):  # 用户重复错误
    status_code = 403
    default_detail = "CategoryNotFound!"


class PullPostSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=256)
    topic = serializers.CharField(source="name")
    images = serializers.ListField()
    content = serializers.CharField(max_length=50000)

    class Meta:
        model = Topic

    def create(self, validated_data):
        topic = Topic.objects.create(name=validated_data["name"], content=validated_data["content"],
                                     uuid=str(uuid.uuid4()))
        try:
            category = Category.objects.get(name=validated_data["category"])
            topic.category = category
            topic.save()
            for u in validated_data["images"]:
                TopicPicture.objects.create(url=u, topic_id=topic)
            return topic
        except:
            raise CategoryNotFoundError


class PullNewCategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class CommentSerializer(serializers.Serializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["content", "num_like", "uuid", "customer"]

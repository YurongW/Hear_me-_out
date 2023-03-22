import uuid

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from Account.auth import ExpiringTokenAuthentication
from Post.models import Category, Topic, RecordLike, Comment
from Post.serializers import PullPostSerializer


class PullTopic(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        user = request.user
        post = PullPostSerializer(data=request.data)
        if post.is_valid():
            topic = post.save()
            topic.customer_id = user
            user.num_post += 1
            user.save()
            topic.save()
            return Response({"status": "success", "details": {"uuid": topic.uuid}})
        else:
            return Response({"status": "failed", "details": post.errors})


class CommentToTopic(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        user = request.user
        topic_uuid = request.data["topic_uuid"]
        content = request.data["content"]
        comment = Comment.objects.create(content=content, uuid=str(uuid.uuid4()))
        comment.customer_id = user
        comment.topic_id = Topic.objects.get(uuid=topic_uuid)
        comment.save()
        comment.topic_id.num_comment += 1
        comment.topic_id.save()
        return Response({"status": "success", "detail": {"comment_id": comment.uuid}})


class PullCategory(APIView):
    permission_classes = [IsAdminUser]

    # authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        if Category.objects.filter(name=request.data["category_name"]).exists():
            return Response({"status": "failed", "detail": "Already exist category!"})
        Category.objects.create(name=request.data["category_name"])
        return Response({"status": "success", "detail": "Created!"})


class ReadPost(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def get(self, request):
        try:
            topic = Topic.objects.get(uuid=request.query_params.get("uuid"))
        except:
            return Response({"status": "failed", "detail": "topic not found"})
        comments = []
        for i in topic.customers_comment.all():
            comments.append({
                "content": i.content,
                "num_like": i.num_like,
                "uuid": i.uuid,
                "customer": i.customer_id.username
            })
        return Response({"status": "success", "detail": {
            "topic": topic.name,
            "images": [img.url for img in topic.topicpicture_set.all()],
            "content": topic.content,
            "comment": comments,
            "customer_name": topic.customer_id.username,
            "num_like": topic.like,
            "category": topic.category.name
        }})


class EditPost(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        user = request.user
        uuid = request.data["uuid"]
        topic_name = request.data['topic']
        content = request.data["content"]
        if user.is_superuser:
            try:
                topic = Topic.objects.get(uuid=uuid)
            except:
                return Response({"status": "failed", "detail": "Topic not found!"})
        else:
            try:
                topic = Topic.objects.get(uuid=uuid, customer_id=user.id)
            except:
                return Response({"status": "failed", "detail": "Not allowed!"})
        topic.name = topic_name
        topic.content = content
        topic.save()
        return Response({"status": "success", "detail": {
            "topic": topic.name,
            "content": topic.content,
            "customer_name": topic.customer_id.username,
            "num_like": topic.like,
            "category": topic.category.name
        }})


class DeletePostComment(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def get(self, request):
        user = request.user
        uuid = request.query_params.get("uuid")
        if user.is_superuser:
            try:
                if Topic.objects.filter(uuid=uuid).count() == 0:
                    Comment.objects.get(uuid=uuid).delete()
                else:
                    Topic.objects.get(uuid=uuid).delete()
                return Response({"status": "success"})
            except:
                return Response({"status": "failed", "detail": "Topic not found!"})
        else:
            try:
                if Topic.objects.filter(uuid=uuid, customer_id=user.id).count() == 0:
                    Comment.objects.get(uuid=uuid, customer_id=user.id).delete()
                else:
                    Topic.objects.get(uuid=uuid, customer_id=user.id).delete()
                return Response({"status": "success"})
            except:
                return Response({"status": "failed", "detail": "Not allowed!"})


class DeleteCategory(APIView):
    permission_classes = [IsAdminUser]

    # authentication_classes = [ExpiringTokenAuthentication]

    def post(self, request):
        category_name = request.data["category_name"]
        try:
            Category.objects.get(name=category_name).delete()
            return Response({"status": "success"})
        except:
            return Response({"status": "false", "detail": "Category not found!"})


class Like(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]

    def get(self, request):
        uuid = request.query_params.get("uuid")
        user = request.user

        if RecordLike.objects.filter(uuid=uuid, customer_id=user.id).count() != 0:
            return Response({"status": "failed", "detail": "Have liked!"})
        try:
            if Topic.objects.filter(uuid=uuid).count() == 0:
                comment = Comment.objects.get(uuid=uuid)
                comment.num_like += 1
                comment.customer_id.num_like += 1
                RecordLike.objects.create(uuid=uuid, customer_id=user.id)
                comment.save()
                comment.customer_id.save()
                return Response({"status": "success"})
            else:
                topic = Topic.objects.get(uuid=uuid)
                topic.like += 1
                topic.customer_id.num_like += 1
                RecordLike.objects.create(uuid=uuid, customer_id=user.id)
                topic.save()
                topic.customer_id.save()
                return Response({"status": "success"})
        except:
            return Response({"status": "failed", "detail": "Topic or comment not found"})


class TopTopics(APIView):
    def get(self, request):
        category = request.query_params.get("category")

        if not category:
            if Topic.objects.all().order_by("-like").count() < 10:
                top = Topic.objects.all().order_by("-like")
            else:
                top = Topic.objects.all().order_by("-like")[:10]
            res_top = []
            for t in top:
                res_top.append({"uuid": t.uuid, "topic-name": t.name, "like": t.like})
            return Response({"status": "success", "detail": res_top})
        else:
            if Topic.objects.filter(category__name=category).count() == 0:
                return Response({"status": "failed", "detail": "No match category! Or no topic in this category"})
            if Topic.objects.filter(category__name=category).order_by("-like").count() < 10:
                top = Topic.objects.filter(category__name=category).order_by("-like")
            else:
                top = Topic.objects.filter(category__name=category).order_by("-like")[:10]
            res_top = []
            for t in top:
                res_top.append({"uuid": t.uuid, "topic-name": t.name, "like": t.like})
            return Response({"status": "success", "detail": res_top})


class AbstractFirstPage(APIView):
    def get(self, request):
        category = request.query_params.get("category")

        if not category:
            topics = Topic.objects.all().order_by("-num_comment")
            res_lst = []
            for t in topics:
                res_lst.append({
                    "topic-name": t.name,
                    "topic-uuid": t.uuid,
                    "images": [img.url for img in t.topicpicture_set.all()],
                    "like": t.like,
                    "category": t.category.name,
                    "customer": t.customer_id.username
                })
            return Response({"status": "success", "detail": res_lst})
        else:
            if Topic.objects.filter(category__name=category).count() == 0:
                return Response({"status": "failed", "detail": "No match category!Or no topic in this category"})
            topics = Topic.objects.filter(category__name=category).order_by("-num_comment")
            res_lst = []
            for t in topics:
                res_lst.append({
                    "topic-name": t.name,
                    "topic-uuid": t.uuid,
                    "images": [img.url for img in t.topicpicture_set.all()],
                    "like": t.like,
                    "category": t.category.name,
                    "customer": t.customer_id.username
                })
            return Response({"status": "success", "detail": res_lst})


class CategoryName(APIView):
    def get(self, request):
        return Response({"status": "success", "detail": [c.name for c in Category.objects.all()]})


class SearchCategory(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        if not q:
            return [c.name for c in Category.objects.all()]
        else:
            if not Topic.objects.filter(category__name=q):
                return Response({"status": "failed", "detail": "Not found!"})
            else:
                res_lst = []
                for t in Topic.objects.filter(category__name=q).order_by("-like"):
                    res_lst.append({
                        "topic-name": t.name,
                        "topic-uuid": t.uuid,
                        "images": [img.url for img in t.topicpicture_set.all()],
                        "like": t.like,
                        "category": t.category.name,
                        "customer": t.customer_id.username
                    })
                return Response({"status": "success", "detail": res_lst})


class SearchTopic(APIView):
    def get(self, request):
        keyword = request.query_params.get('q')
        if not keyword:
            return Response({"status": "Not found"})
        else:
            query = Topic.objects.filter(name=keyword)
            if query:
                res_lst = []
                for t in Topic.objects.filter(name=keyword).order_by("-like"):
                    res_lst.append({
                        "topic-name": t.name,
                        "topic-uuid": t.uuid,
                        "images": [img.url for img in t.topicpicture_set.all()],
                        "like": t.like,
                        "category": t.category.name,
                        "customer": t.customer_id.username
                    })
                return Response({"status": "success", "detail": res_lst})
            else:
                return Response({"status": "Not found"})


class EditCategory(APIView):
    def get(self, request):
        old = request.query_params.get('old')
        new = request.query_params.get('new')
        ca = Category.objects.get(name=old)
        try:
            ca.name = new
            ca.save()
            return Response({"status": "success", "detail": "Created!"})
        except:
            return Response({"status": "failed", "detail": "Already exist category!"})

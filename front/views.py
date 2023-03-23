from django.shortcuts import render

from Account.models import Account
from Account.serializers import AccountInformationSerializer
from Post.models import Topic, Category


def get_top10_category():
    if Topic.objects.all().order_by("-like").count() < 10:
        top = Topic.objects.all().order_by("-like")
    else:
        top = Topic.objects.all().order_by("-like")[:10]
    res_top = []
    for t in top:
        res_top.append({"uuid": t.uuid, "topicname": t.name, "like": t.like})
    # return Response({"status": "success", "detail": res_top})

    return {"top10": res_top, "category": [c.name for c in Category.objects.all()]}


# Create your views here.
def index(request):
    res = get_top10_category()
    topics = Topic.objects.all().order_by("-num_comment")
    res_lst = []
    for t in topics:
        res_lst.append({
            "topicname": t.name,
            "topicuuid": t.uuid,
            "images": [img.url for img in t.topicpicture_set.all()],
            "like": t.like,
            "category": t.category.name,
            "customer": t.customer_id.username,
            "content": t.content
        })
    res["posts"] = res_lst
    return render(request, "index.html",
                  context=res)


def PopularPost(request, category):
    res = get_top10_category()
    topics = Topic.objects.filter(category__name=category).order_by("-num_comment")
    res_lst = []
    for t in topics:
        res_lst.append({
            "topicname": t.name,
            "topicuuid": t.uuid,
            "images": [img.url for img in t.topicpicture_set.all()],
            "like": t.like,
            "category": t.category.name,
            "customer": t.customer_id.username,
            "content": t.content
        })
    res["posts"] = res_lst
    res["name"] = category
    return render(request, "category.html",
                  context=res)


def ReadPost(request):
    return render(request, "test.html")


def personal_page(request):
    user = request.user
    info = AccountInformationSerializer(user).data
    comment = Account.objects.get(id=user.id).customers_comment.all()[::-1]
    res_lst = []
    for c in comment:
        res_lst.append({
            "topic_name": c.topic_id.name,
            "topic_uuid": c.topic_id.uuid,
            "comment_uuid": c.uuid,
            "numlike": c.num_like,
            "content": c.content,
            "images": []
        })
    topic = Account.objects.get(id=user.id).customers.all()[::-1]
    for t in topic:
        res_lst.append({
            "topic_name": t.name,
            "topic_uuid": t.uuid,
            "comment_uuid": t.uuid,
            "numlike": t.like,
            "content": t.content,
            "images": [img.url for img in t.topicpicture_set.all()]
        })
    # print(res_lst)
    return render(request, "account.html", context={"info": info, "res": res_lst})


def ReadContent(request, uuid):
    user = request.user
    topic = Topic.objects.get(uuid=uuid)
    comments = []
    for i in topic.customers_comment.all():
        comments.append({
            "content": i.content,
            "num_like": i.num_like,
            "uuid": i.uuid,
            "customer": i.customer_id.username,
            "avatar": i.customer_id.avatar
        })
    res = get_top10_category()
    res["topicuuid"] = topic.uuid
    res["topic"] = topic.name
    res["images"] = [img.url for img in topic.topicpicture_set.all()]
    res["content"] = topic.content
    res["comment"] = comments
    res["customer_name"] = topic.customer_id.username
    res["num_like"] = topic.like
    return render(request, "content.html", context=res)


def ManageCategory(request):
    user = request.user
    if not user.is_superuser:
        return render(request, "administrator.html")
    else:
        res = get_top10_category()
        return render(request, "administrator.html", context=res)

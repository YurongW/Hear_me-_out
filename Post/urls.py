from django.urls import path

from Post.views import PullTopic, PullCategory, ReadPost, EditPost, DeleteCategory, DeletePostComment, Like, TopTopics, \
    CommentToTopic, AbstractFirstPage, CategoryName, SearchCategory, SearchTopic, EditCategory

urlpatterns = [
    path('pull_topic/', PullTopic.as_view()),
    path("create_category/", PullCategory.as_view()),
    path("readpost/", ReadPost.as_view(), name="read"),
    path("edit/", EditPost.as_view()),
    path("delete_post_comment/", DeletePostComment.as_view()),
    path("delete_category/", DeleteCategory.as_view()),
    path("like/", Like.as_view()),
    path("top10/", TopTopics.as_view()),
    path("comment/", CommentToTopic.as_view()),
    path("popular_post/", AbstractFirstPage.as_view()),
    path("category_name/", CategoryName.as_view()),
    path("search_category/", SearchCategory.as_view()),
    path("search_topic/", SearchTopic.as_view()),
    path("edit_category/", EditCategory.as_view())
]

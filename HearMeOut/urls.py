"""HearMeOut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from HearMeOut import settings
from Picbed.views import UploadImg
from front.views import index, PopularPost, personal_page, ReadContent, ManageCategory



urlpatterns = [
    path('admin/', admin.site.urls),
    path("customer/", include("Account.urls")),
    path("post/", include("Post.urls")),
    path("uploadimg/", UploadImg.as_view()),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    # re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("index/", index, name="index"),
    # path("topic/", topic, name="topic"),
    path("popularpost/<category>/", PopularPost, name="popular"),
    path("personal/", personal_page, name="personal"),
    path("content/<uuid>/", ReadContent, name="content"),
    path("manage/", ManageCategory, name="manage")
]

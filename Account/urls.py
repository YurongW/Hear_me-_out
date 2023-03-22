# HearMeOut
# -*- coding: UTF-8 -*-
"""
@Project ：HearMeOut 
@File    ：urls.py
@IDE     ：PyCharm 
@Author  ：ZYM
@Date    ：2023-03-03 8:34 
"""
from django.urls import path

from Account.views import Register, Login, Logout, DeleteCustomer, CustomerInformation, CreateAdmin, HistoryPost

urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("delete/", DeleteCustomer.as_view()),
    path("information/", CustomerInformation.as_view()),
    path("create_admin/", CreateAdmin.as_view()),
    path("personal_history/", HistoryPost.as_view())
]

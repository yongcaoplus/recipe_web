# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 3:54 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 通过用户名或邮箱来获取用户对象
            user = User.objects.get(
                Q(username=username) |
                Q(email=username )
            )
            return user
        except Exception:
            return None

from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class UserLogoutView(LogoutView):
    # 用户退出登录后，将要跳转的 URL
    next_page = reverse_lazy('users:login')
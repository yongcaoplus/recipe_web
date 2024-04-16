"""recipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from myapp import views
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('adapt_en2cn/', views.adapt_en2cn, name='adapt_en2cn'),
    path('adapt_en2cn_admin/', views.adapt_en2cn_admin, name='adapt_en2cn_admin'),
    path('adapt_cn2en/', views.adapt_cn2en, name='adapt_cn2en'),
    path('adapt_example/', views.adapt_example, name='adapt_example'),
    path('evaluate_en2cn/', views.evaluate_en2cn, name='evaluate_en2cn'),
    path('evaluate_example/', views.evaluate_example, name='evaluate_example'),
    path('evaluate_cn2en/', views.evaluate_cn2en, name='evaluate_cn2en'),
    path('loginin/', views.loginin, name='loginin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('check_email/', views.check_email, name='check_email'),
    path('register_user/', views.register_user, name='register_user'),
    path('get_user_progress/', views.get_user_progress, name='get_user_progress'),
    path('get_user_evaluation_num/', views.get_user_evaluation_num, name='get_user_evaluation_num'),
    path('submit_adapt/', views.submit_adapt, name='submit_adapt'),
    path('submit_adapt_admin/', views.submit_adapt_admin, name='submit_adapt_admin'),
    path('submit_evaluation/', views.submit_evaluation, name='submit_evaluation'),
    re_path(r'^\.well-known/pki-validation/(?P<path>.*)$', serve, {
        'document_root': '/home/cy/recipe_web/myapp/templates/.well-known/pki-validation/',
    }),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    path('evaluate_compre_cn2en/', views.evaluate_compre_cn2en, name='evaluate_compre_cn2en'),
    path('evaluate_compre_en2cn/', views.evaluate_compre_en2cn, name='evaluate_compre_en2cn'),
    path('stop_evaluation/', views.stop_evaluation, name='stop_evaluation'),
    path('submit_comprehension/', views.submit_comprehension, name='submit_comprehension'),
    path('tutorial/', views.tutorial_video, name='tutorial_video'),
    path('evaluate_tutorial/', views.evaluate_tutorial, name='evaluate_tutorial'),

    path('gpt4_compre_cn_1996/', views.gpt4_compre_cn_1996, name='gpt4_compre_cn_1996'),
    path('submit_compre_cn_1996/', views.submit_compre_cn_1996, name='submit_compre_cn_1996'),
    path('gpt4_evaluate_cn_1996/', views.gpt4_evaluate_cn_1996, name='gpt4_evaluate_cn_1996'),
    path('submit_evaluation_cn_1996/', views.submit_evaluation_cn_1996, name='submit_evaluation_cn_1996'),
    path('get_user_gpt4_evaluation_num/', views.get_user_gpt4_evaluation_num, name='get_user_gpt4_evaluation_num'),

    path('gpt4_compre_id_01/', views.gpt4_compre_id_01, name='gpt4_compre_id_01'),
    path('submit_compre_id_01/', views.submit_compre_id_01, name='submit_compre_id_01'),
    path('gpt4_evaluate_id_01/', views.gpt4_evaluate_id_01, name='gpt4_evaluate_id_01'),
    path('submit_evaluation_id_01/', views.submit_evaluation_id_01, name='submit_evaluation_id_01'),
    path('get_user_gpt4_evaluation_num/', views.get_user_gpt4_evaluation_num, name='get_user_gpt4_evaluation_num'),

    path('gpt4_compre_sw_27/', views.gpt4_compre_sw_27, name='gpt4_compre_sw_27'),
    path('submit_compre_sw_27/', views.submit_compre_sw_27, name='submit_compre_sw_27'),
    path('gpt4_evaluate_sw_27/', views.gpt4_evaluate_sw_27, name='gpt4_evaluate_sw_27'),
    path('submit_evaluation_sw_27/', views.submit_evaluation_sw_27, name='submit_evaluation_sw_27'),
    path('get_user_gpt4_evaluation_num/', views.get_user_gpt4_evaluation_num, name='get_user_gpt4_evaluation_num'),

    path('gpt4_compre_ta_20/', views.gpt4_compre_ta_20, name='gpt4_compre_ta_20'),
    path('submit_compre_ta_20/', views.submit_compre_ta_20, name='submit_compre_ta_20'),
    path('gpt4_evaluate_ta_20/', views.gpt4_evaluate_ta_20, name='gpt4_evaluate_ta_20'),
    path('submit_evaluation_ta_20/', views.submit_evaluation_ta_20, name='submit_evaluation_ta_20'),
    path('get_user_gpt4_evaluation_num/', views.get_user_gpt4_evaluation_num, name='get_user_gpt4_evaluation_num'),
    
    path('gpt4_compre_tr_23/', views.gpt4_compre_tr_23, name='gpt4_compre_tr_23'),
    path('submit_compre_tr_23/', views.submit_compre_tr_23, name='submit_compre_tr_23'),
    path('gpt4_evaluate_tr_23/', views.gpt4_evaluate_tr_23, name='gpt4_evaluate_tr_23'),
    path('submit_evaluation_tr_23/', views.submit_evaluation_tr_23, name='submit_evaluation_tr_23'),
    path('get_user_gpt4_evaluation_num/', views.get_user_gpt4_evaluation_num, name='get_user_gpt4_evaluation_num'),
    
    path('gpt4_filter_tr', views.gpt4_filter_tr, name='gpt4_filter_tr'),
    path('gpt4_filter_ta', views.gpt4_filter_ta, name='gpt4_filter_ta'),
    path('gpt4_filter_id', views.gpt4_filter_id, name='gpt4_filter_id'),
    path('gpt4_filter_sw', views.gpt4_filter_sw, name='gpt4_filter_sw'),
    path('get_user_gpt4_filter_num', views.get_user_gpt4_filter_num, name='get_user_gpt4_filter_num'),
    path('submit_filter', views.submit_filter, name='submit_filter')
]

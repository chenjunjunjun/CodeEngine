#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-4-4 下午4:45
# @Author  : 无敌小龙虾
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^question/$', views.QuestionList.as_view()),
    url(r'^question/(?P<pk>[0-9]+)/$', views.QuestionDetailList.as_view()),
    url(r'^knowledge/$', views.KnowledgeList.as_view()),
    url(r'^knowledge/(?P<pk>[0-9]+)/$', views.KnoledgeDetailList.as_view()),
    url(r'^auth/$', views.UserAuthView),
    url(r'^userview/$', views.UserView),
    url(r'^rank/$', views.RankList.as_view()),
    url(r'^update/$', views.UpdateRankView),
    url(r'^knowledge/chapter/(?P<pk>[0-9]+)/$', views.ChapterView.as_view(), name='chapter-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

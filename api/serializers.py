#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-4-4 下午7:43
# @Author  : 无敌小龙虾
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers

from api.models import Answers, User, QuestionSet, Knowledge, Chapter, Attribute


class AnswersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('order', 'answer_choice')


class AttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('user_choose', 'choose_status')


class QuestionSetSerializers(serializers.ModelSerializer):
    answers = serializers.StringRelatedField(many=True, read_only=True)
    attribute = AttributeSerializers(many=True, read_only=True)

    class Meta:
        model = QuestionSet
        fields = ('id', 'type', 'question', 'answers', 'right_answer',
                  'attribute')


class ChapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'chapter_title', 'content')


class ChapterTwoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'chapter_title')


class KnowledgeSerializers(serializers.ModelSerializer):
    # chapter = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='chapter-detail')

    # chapter = serializers.StringRelatedField(many=True, read_only=True)
    chapter = ChapterTwoSerializers(many=True, read_only=True)

    class Meta:
        model = Knowledge
        fields = ('id', 'type', 'chapter')


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'session', 'nick_name', 'avatar')


class RankSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nick_name', 'answer_score', 'avatar')

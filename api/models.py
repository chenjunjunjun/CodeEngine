from django.db import models

# Create your models here.

# class AnswerCount(models.Model):
#     answer_score = models.IntegerField(default=0)
#     answer_counting = models.CharField(max_length=128, default='0')
#
#     def __str__(self):
#         return self.answer_counting


class User(models.Model):
    openid = models.CharField(max_length=128, unique=True)
    session = models.CharField(max_length=255, unique=True)
    weapp_session = models.CharField(max_length=255, unique=True)
    nick_name = models.CharField(max_length=128, blank=True)
    avatar = models.CharField(max_length=128, blank=True)
    answer_score = models.IntegerField(default=0)
    answer_counting = models.CharField(max_length=128, default='0')

    # answer_count = models.OneToOneField(AnswerCount, on_delete=models.CASCADE)

    def __str__(self):
        return self.nick_name if self.nick_name else self.openid


class Knowledge(models.Model):
    type = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.type


class Chapter(models.Model):
    Knowledge = models.ForeignKey(
        Knowledge, related_name='chapter', on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return self.chapter_title


class QuestionSet(models.Model):
    type = models.CharField(max_length=128, blank=False)
    question = models.CharField(max_length=255, default="")
    right_answer = models.CharField(max_length=32, default='')

    def __str__(self):
        return '%s: %s' % (self.type, self.question)


class Attribute(models.Model):
    question = models.ForeignKey(QuestionSet, related_name='attribute')
    user_choose = models.CharField(max_length=16, default='')
    choose_status = models.BooleanField()

    def __str__(self):
        return self.user_choose


class Answers(models.Model):
    question = models.ForeignKey(
        QuestionSet, related_name='answers', on_delete=models.CASCADE)
    answer_choice = models.CharField(max_length=128, default='')
    order = models.IntegerField()

    class Meta:
        unique_together = ('question', 'order')
        ordering = [
            'order',
        ]

    def __str__(self):
        return self.answer_choice

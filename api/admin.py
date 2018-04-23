from django.contrib import admin
from api.models import *

# Register your models here.

# admin.site.register(AnswerCount)
admin.site.register(User)
admin.site.register(Knowledge)
admin.site.register(QuestionSet)
admin.site.register(Answers)
admin.site.register(Chapter)
admin.site.register(Attribute)
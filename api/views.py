from api.models import User, Knowledge, QuestionSet, Chapter
from api.serializers import QuestionSetSerializers, KnowledgeSerializers, RankSerializers, ChapterSerializers
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
import random
from .Wechat import get_session_key
from django.http import JsonResponse


# Create your views here.

class QuestionList(generics.ListAPIView):
    # queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializers

    def get_queryset(self):
        queryset = QuestionSet.objects.all()
        qtype = self.request.query_params.get('type', None)
        if qtype is not None:
            queryset = queryset.filter(type=qtype).order_by('?')[:20]
        return queryset


class QuestionDetailList(generics.RetrieveAPIView):
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializers


class KnowledgeList(generics.ListAPIView):
    # queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializers

    def get_queryset(self):
        queryset = Knowledge.objects.all()
        ktype = self.request.query_params.get('type', None)
        if ktype is not None:
            queryset = queryset.filter(type=ktype)
        return queryset


class KnoledgeDetailList(generics.RetrieveAPIView):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializers


def generate_session(count=64):
    ran = "".join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890'
                                'zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlk'
                                'jihgfedcba', count)).replace(" ", "")
    return ran


@csrf_exempt
def UserAuthView(request):
    if request.method == 'GET':
        session = request.GET.get('session')
        user = User.objects.filter(session=session)
        if user.exists():
            return JsonResponse({
                'status': 200,
                'msg': 'success',
            })
        return JsonResponse({
            'status': 404,
            'msg': 'session 不存在或过期',
        })

    if request.method == 'POST':
        code = request.POST.get('code', None)
        # data = json.loads(request)
        # code = data.get('code', '').strip()
        if code:
            status, openid, session = get_session_key(code)
            if status:
                my_session = generate_session()
                user = User.objects.filter(openid=openid)
                if user.exists():
                    user = user[0]
                    user.weapp_session = session
                    user.session = my_session
                    user.save()
                else:
                    User(openid=openid, weapp_session=session, session=my_session).save()
                return JsonResponse({
                    'body': {
                        'session': my_session,
                    },
                    'status': 201,
                    'msg': 'success',
                })
            return JsonResponse({
                'msg': 'code 错误',
                'status': 101,
            })
        return JsonResponse({
            'msg': 'code 缺失',
            'status': 100,
        })


@csrf_exempt
def UserView(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        user = User.objects.filter(session=session)
        if user.exists():
            user = user[0]
            if not user.nick_name:
                user.nick_name = request.POST.get('nickName')
                user.avatar = request.POST.get('avatarUrl')
                user.save()
            return JsonResponse({
                'status': 200,
                'msg': 'success',
            })
        return JsonResponse({
            'status': 404,
            'msg': 'session 已过期或不存在',
        })

    if request.method == 'GET':
        session = request.GET.get('session')
        user = User.objects.filter(session=session)
        if user.exists():
            user = user[0]
            return JsonResponse({
                'status': 200,
                'msg': 'success',
                'avatar': user.avatar,
                'nick_name': user.nick_name,
            })

        else:
            return JsonResponse({
                'status': 404,
                'msg': 'session已过期或不存在',
            })


class RankList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-answer_score')
    serializer_class = RankSerializers


@csrf_exempt
def UpdateRankView(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        answer_score = request.POST.get('answer_score')
        answer_counting = request.POST.get('answer_counting')
        user = User.objects.filter(session=session)
        if user.exists():
            user = user[0]
            user.answer_score += int(answer_score)
            user.answer_counting = answer_counting
            user.save()
            return JsonResponse({
                'status': 200,
                'msg': 'success',
            })
        return JsonResponse({
            'status': 400,
            'msg': 'session不存在或已过期',
        })


class ChapterView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializers

# 필요한 모듈
# PyJWT, py-bcrypt, djangorestframework, django-rest-auth

import json
import bcrypt
import jwt

from westa_posting.settings import SECRET_KEY
from .models import Account

from django.views import View
from django.http import JsonResponse, HttpResponse

from account.authentication import JSONWebTokenAuthentication


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            # 존재하는 userid인지 확인
            if Account.objects.filter(userid=data['userid']).exists():
                return JsonResponse({'message': 'userid duplicate'}, status=400)

            #== 비밀번호 암호화==#

            password = data['password'].encode(
                'utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
            password_crypt = bcrypt.hashpw(
                password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
            # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
            # password_crypt = password_crypt.decode('utf-8')

            #====================#

            # DB 저장
            Account(
                userid=data['userid'],
                password=password_crypt                               # 암호화된 비밀번호를 DB에 저장
            ).save()

            #----------토큰 발행----------#

            token = jwt.encode(
                {'userid': data['userid']}, SECRET_KEY, algorithm="HS256")
            token = token.decode('utf-8')      # 유니코드 문자열로 디코딩

            #-----------------------------#

            return JsonResponse({"token": token, "user": data}, status=200)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(userid=data['userid']).exists():
                user = Account.objects.get(userid=data['userid'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):

                    #----------토큰 발행----------#

                    token = jwt.encode(
                        {'userid': data['userid']}, SECRET_KEY, algorithm="HS256")
                    token = token.decode('utf-8')      # 유니코드 문자열로 디코딩

                    #-----------------------------#
                    return JsonResponse({"token": token, "user": data}, status=200)

                else:
                    return JsonResponse({'message': '비밀번호가 틀렸어요'}, status=401)

            return JsonResponse({'message': '등록되지 않은 이메일 입니다.'}, status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


class UserDelete(View):
    def delete(self, request):
        data = json.loads(request.body)

        if Account.objects.filter(userid=data['userid']).exists():
            # 인증하기
            auth = request.META.get("HTTP_AUTHORIZATION")
            if auth != None:
                list_1 = auth.split(" ")

                user_token_info = jwt.decode(
                    list_1[1], SECRET_KEY, algorithm='HS256')

                if Account.objects.filter(userid=user_token_info['userid']).exists():
                    user = Account.objects.get(userid=data['userid'])
                    user.delete()
                    return JsonResponse({'message': '삭제 성공'}, status=200)
            else:
                return JsonResponse({'message': '토큰 없음'}, status=400)
        elif Account.objects.filter(userid=data['userid']) == None:
            return JsonResponse({'message': '아이디 없음'}, status=400)
        else:
            return JsonResponse({'message': '아이디 틀림'}, status=400)


class TokenCheckView(View):
    def post(self, request):
        data = json.loads(request.body)

        user_token_info = jwt.decode(
            data['token'], SECRET_KEY, algorithm='HS256')

        if Account.objects.filter(userid=user_token_info['userid']).exists():
            return JsonResponse({'message': '유저 정보가 DB에 있는 정보와 일치'}, status=200)
        else:
            return JsonResponse({'message': '사용자 거부'}, status=403)

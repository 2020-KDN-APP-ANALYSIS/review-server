# 필요한 모듈
# PyJWT, py-bcrypt, djangorestframework, django-rest-auth

import json
import bcrypt
import jwt

# from re_view.config.settings.base import JWT_AUTH
from django.conf import settings
from .models import Account

from django.views import View
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from account.authentication import JSONWebTokenAuthentication
from .serializers import AccountSerializer


class SignUpView(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def post(self, request):
        data = json.loads(request.body)
        try:
            # 존재하는 userid인지 확인
            if Account.objects.filter(userid=data['userid']).exists():
                return JsonResponse({'code': '400', 'message': 'userid duplicate'}, status=400)

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
                password=password_crypt,                           # 암호화된 비밀번호를 DB에 저장
                user_name=data['user_name'],
                gender=data['gender'],
                user_email=data['user_email'],
                phonenumber=data['phonenumber']
            ).save()

            #----------토큰 발행----------#

            token = jwt.encode(
                {'userid': data['userid']}, self.JWT_SECRET_KEY, algorithm="HS256")
            token = token.decode('utf-8')      # 유니코드 문자열로 디코딩

            #-----------------------------#

            user = Account.objects.filter(userid=data['userid']).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
            return HttpResponse(json.dumps({"token": token, "user": list(user)}), content_type="application/json")

        except KeyError:
            return JsonResponse({'code': '400', "message": "INVALID_KEYS"}, status=400)


class SignInView(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(userid=data['userid']).exists():
                user = Account.objects.get(userid=data['userid'])
                

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):

                    #----------토큰 발행----------#

                    token = jwt.encode(
                        {'userid': data['userid']}, self.JWT_SECRET_KEY, algorithm="HS256")
                    token = token.decode('utf-8')      # 유니코드 문자열로 디코딩

                    #-----------------------------#

                    user_1 = Account.objects.filter(userid=data['userid']).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
                    return HttpResponse(json.dumps({"token": token, "user": list(user_1)}), content_type="application/json")

                else:
                    return JsonResponse({'code': '401' ,'message': 'The password is wrong'}, status=401)

            return JsonResponse({'code': '401' ,'message': 'This email is not registered'}, status=401)

        except KeyError:
           return JsonResponse({'code': '400', "message": "INVALID_KEYS"}, status=400)


class UserDelete(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def delete(self, request):
        # 토큰 검사하기
        auth = request.META.get("HTTP_AUTHORIZATION")

        if auth != None:
            list_1 = auth.split(" ")

            user_token_info = jwt.decode(
                list_1[1], self.JWT_SECRET_KEY, algorithm='HS256')

            if Account.objects.filter(userid=user_token_info['userid']).exists():
                # 토큰 있음
                data = json.loads(request.body)

                if Account.objects.filter(userid=data['userid']).exists():
                    user = Account.objects.get(userid=data['userid'])
                    user.delete()
                    return JsonResponse({'code': '200', 'message': 'Delete success'}, status=200)
                else:
                    return JsonResponse({'code': '401', 'message': 'Incorrect userid'}, status=401)
        else:
            return JsonResponse({'code': '401', 'message': 'Token is empty'}, status=401)


class User_view(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def get(self, request, account_id):
        # 토큰 검사하기
        auth = request.META.get("HTTP_AUTHORIZATION")

        if auth != None:
            list_1 = auth.split(" ")

            user_token_info = jwt.decode(
                list_1[1], self.JWT_SECRET_KEY, algorithm='HS256')
            
            token = list_1[1]

            if Account.objects.filter(userid=user_token_info['userid']).exists():
                user = Account.objects.filter(userid=account_id).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
                return HttpResponse(json.dumps({"token": token, "user": list(user)}), content_type="application/json")
        else:
            return JsonResponse({'code': '401', 'message': 'Token is empty'}, status=401)


class ChangeUserALL(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def patch(self, request, account_id):
        try:
            data = json.loads(request.body)

            # 토큰 검사하기
            auth = request.META.get("HTTP_AUTHORIZATION")

            if auth != None:
                list_1 = auth.split(" ")

                user_token_info = jwt.decode(
                    list_1[1], self.JWT_SECRET_KEY, algorithm='HS256')

                token = list_1[1]

                if Account.objects.filter(userid=user_token_info['userid']).exists():
                    Account.objects.filter(userid=account_id).values('user_name', 'gender', 'phonenumber', 'user_email').update(
                        user_name=data['new_user_name'],
                        gender=data['new_gender'],
                        user_email=data['new_user_email'],
                        phonenumber=data['new_phonenumber']
                    )
                    user = Account.objects.filter(userid=account_id).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
                    return HttpResponse(json.dumps({'code': '200', 'token': token, 'user': list(user)}), content_type="application/json")
            else:
                return JsonResponse({'code': '401', 'message': 'Token is empty'}, status=401)

        except KeyError:
            return JsonResponse({'code': '400', "message": "INVALID_KEYS"}, status=400)


class ChangePassword(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def post(self, request, account_id):
        try:
            data = json.loads(request.body)

            # 토큰 검사하기
            auth = request.META.get("HTTP_AUTHORIZATION")

            if auth != None:
                list_1 = auth.split(" ")

                user_token_info = jwt.decode(
                    list_1[1], self.JWT_SECRET_KEY, algorithm='HS256')

                token = list_1[1]

                if Account.objects.filter(userid=user_token_info['userid']).exists():
                    #== 비밀번호 암호화==#

                    password = data['new_password'].encode('utf-8')                 # 입력된 패스워드를 바이트 형태로 인코딩
                    password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())  # 암호화된 비밀번호 생성
                    # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
                    # password_crypt = password_crypt.decode('utf-8')
                    #====================#

                    Account.objects.filter(userid=account_id).values('password').update(
                        password=password_crypt
                    )
                    user = Account.objects.filter(userid=account_id).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
                    return HttpResponse(json.dumps({'code': '200', 'message': 'Password change successful', 'token': token, 'user': list(user)}), content_type="application/json")
            else:
                return JsonResponse({'code': '401', 'message': 'Token is empty'}, status=401)

        except KeyError:
            return JsonResponse({'code': '400', "message": "INVALID_KEYS"}, status=400)


class TokenCheckView(View):
    def __init__(self):
        USER_SETTINGS = getattr(settings, "JWT_AUTH", None)

        self.JWT_SECRET_KEY = USER_SETTINGS["JWT_SECRET_KEY"]
        self.JWT_ALGORITHM = USER_SETTINGS["JWT_ALGORITHM"]

    def get(self, request):
        # data = json.loads(request.body)
        auth = request.META.get("HTTP_AUTHORIZATION")

        list_1 = auth.split(" ")

        user_token_info = jwt.decode(
            list_1[1], self.JWT_SECRET_KEY, algorithm='HS256')

        token = list_1[1]

        if Account.objects.filter(userid=user_token_info['userid']).exists():
            user = Account.objects.filter(userid=user_token_info['userid']).values('userid', 'user_name', 'gender', 'phonenumber', 'user_email')
            return HttpResponse(json.dumps({'code': '200', 'message': 'Authorization authentication success', 'token': token, 'user': list(user)}), content_type="application/json")
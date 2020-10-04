from django.urls import path
from django.conf.urls import url
from .views import SignUpView, SignInView, TokenCheckView, UserDelete, ALL_user

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/token-check', TokenCheckView.as_view()),
    path('/user-del', UserDelete.as_view()),
    path('/user', ALL_user.as_view())
]

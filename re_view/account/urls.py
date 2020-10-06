from django.urls import path
from django.conf.urls import url
from .views import SignUpView, SignInView, TokenCheckView, UserDelete, User_view, ChangeUserALL, ChangePassword

urlpatterns = [
    path('sign-up', SignUpView.as_view()),
    path('sign-in', SignInView.as_view()),
    path('token-check', TokenCheckView.as_view()),
    path('user-del', UserDelete.as_view()),
    path('user/<str:account_id>' , User_view.as_view()),
    path('user/change/<str:account_id>', ChangeUserALL.as_view()),
    path('user/change/passwd/<str:account_id>', ChangePassword.as_view()),
]
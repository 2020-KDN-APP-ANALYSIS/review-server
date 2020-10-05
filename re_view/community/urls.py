from rest_framework import routers
from django.urls import path, include
from .views import (
    PostViewSet,
    AnswerViewSet,
    GetPostAPI,
)

router = routers.DefaultRouter()
router.register(r'talk', PostViewSet, basename="talk")
router.register(r'answer', AnswerViewSet, basename="answer")


urlpatterns = [
    path('', include(router.urls)),
    path('<user_id>', GetPostAPI.as_view())
]

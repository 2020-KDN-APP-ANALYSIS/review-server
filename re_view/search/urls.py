from django.urls import path, include
from .views import (icon_view, title_view , publisher_view , description_view , matrials_view , app_total_view)

urlpatterns = [
    path('apps/<str:app_id>/icon', icon_view),
    path('apps/<str:app_id>/title', title_view),
    path('apps/<str:app_id>/publisher', publisher_view),
    path('apps/<str:app_id>/description', description_view),
    path('apps/<str:app_id>/matrials', matrials_view),
    path('apps/<str:app_id>', app_total_view),
]
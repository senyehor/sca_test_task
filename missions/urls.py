from django.urls import path

from missions.views import MissionViewSet

urlpatterns = [
    path('missions/', MissionViewSet.as_view({'post': 'create'}))
]

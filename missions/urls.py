from django.urls import path

from missions.views import MissionViewSet

urlpatterns = [
    path('missions/', MissionViewSet.as_view({'post': 'create', 'get': 'list'})),
    path(
        'missions/<int:pk>/',
        MissionViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})
    )
]

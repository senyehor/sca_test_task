from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from missions.views import MissionViewSet, TargetNoteViewSet, TargetUpdateView

router = SimpleRouter()

router.register('missions', MissionViewSet)

missions_router = NestedSimpleRouter(router, r'missions', lookup='mission')
missions_router.register(r'targets', TargetUpdateView, basename='mission-target')

targets_router = NestedSimpleRouter(missions_router, 'targets', lookup='target')
targets_router.register('notes', TargetNoteViewSet, basename='target-notes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(missions_router.urls)),
    path('', include(targets_router.urls))
]

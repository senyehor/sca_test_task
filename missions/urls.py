from django.urls import include, path
from rest_framework.routers import SimpleRouter

from missions.views import MissionViewSet

router = SimpleRouter()

router.register('missions', MissionViewSet)

urlpatterns = [
    path('', include(router.urls))
]

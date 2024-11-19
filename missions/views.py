from rest_framework.viewsets import ModelViewSet

from missions.models import Mission
from missions.serializers import MissionSerializer


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

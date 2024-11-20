from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.exceptions import (
    NotFound, ValidationError as DRFValidationError,
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from missions.models import Mission, Target
from missions.serializers import MissionSerializer, TargetSerializer
from utils.restrict_methods_for_view_set_method import restrict_methods


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @method_decorator(atomic)
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message)

    @restrict_methods(('PUT',), message='Mission should be updated using PATCH')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class TargetUpdateView(UpdateModelMixin, GenericViewSet):
    serializer_class = TargetSerializer

    def get_object(self):
        mission_pk = self.kwargs['mission_pk']
        if not Mission.objects.filter(id=mission_pk).exists():
            raise NotFound(f'There is no mission with id {mission_pk}')
        return get_object_or_404(Target, id=self.kwargs['pk'], mission_id=mission_pk)

    @restrict_methods(('PUT',), message='Target should be updated using PATCH')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

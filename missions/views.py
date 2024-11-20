from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
)
from rest_framework.viewsets import ModelViewSet

from missions.models import Mission
from missions.serializers import MissionSerializer
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

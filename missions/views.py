from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework.exceptions import MethodNotAllowed, ValidationError as DRFValidationError
from rest_framework.viewsets import ModelViewSet

from missions.models import Mission
from missions.serializers import MissionSerializer


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @method_decorator(atomic)
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            # DRF considers PUT to have all model's fields and throws an exception
            # when only some of them are included,
            # which is the desired behavior of updating a mission
            raise MethodNotAllowed('PUT', detail='Mission should be updated using PATCH')
        return super().update(request, *args, **kwargs)

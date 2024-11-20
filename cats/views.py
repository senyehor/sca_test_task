from django.db import IntegrityError
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import SpyCat
from .serializers import SpyCatSerializer


class SpyCatListCreateView(generics.ListCreateAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class SpyCatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    @method_decorator(atomic)
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(
                'Failed to delete cat due to db integrity error, '
                'there probably are some dependent objects'
            ) from e

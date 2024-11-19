from rest_framework import generics

from .models import SpyCat
from .serializers import SpyCatSerializer


class SpyCatListCreateView(generics.ListCreateAPIView):
    # todo add pagination
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class SpyCatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

from django.urls import path

from cats.views import SpyCatDetailView, SpyCatListCreateView

urlpatterns = [
    path('spy-cats/', SpyCatListCreateView.as_view(), name='spycat-list-create'),
    path('spy-cats/<int:pk>/', SpyCatDetailView.as_view(), name='spycat-retrieve-update-delete'),
]

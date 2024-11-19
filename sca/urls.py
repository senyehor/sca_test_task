from django.urls import include, path

urlpatterns = [
    path('api/', include('cats.urls')),
    path('api/', include('missions.urls'))
]

from django.urls import path
from .views import map_view, api_vehicules

urlpatterns = [
    path('map/', map_view, name='map'),
    path('api/vehicules/', api_vehicules, name='api_vehicules'),
]
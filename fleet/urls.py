from django.urls import path
<<<<<<< Updated upstream
from .views import map_view, api_vehicules  
=======
from .views import map_view, api_vehicules
>>>>>>> Stashed changes

urlpatterns = [
    path('map/', map_view, name='map'),
    path('api/vehicules/', api_vehicules, name='api_vehicules'),
]
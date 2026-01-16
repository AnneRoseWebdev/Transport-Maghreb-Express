from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, TrajetViewSet, map_view, calculate_route

# Le routeur crée automatiquement les URLs (GET, POST, etc.)
router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet)
router.register(r'trajets', TrajetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('map/', map_view, name='map_view'), # URL de /api/map/
]
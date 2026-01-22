from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculeViewSet, map_view, api_calculate_route

router = DefaultRouter()
router.register(r'vehicules', VehiculeViewSet)

urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    path('api/route/', api_calculate_route, name='api_route'),
    
    # Vue Frontend
    path('map/', map_view, name='map'),
]
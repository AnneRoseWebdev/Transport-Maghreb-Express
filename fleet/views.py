from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response # Plus puissant que JsonResponse
from .models import Vehicule, Trajet
from .serializers import VehiculeSerializer
from .utils import get_shortest_path, CITIES_COORDS 

# 1. API REST Standard (CRUD)
class VehiculeViewSet(viewsets.ModelViewSet):
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer

# 2. Vue HTML
def map_view(request):
    return render(request, 'fleet/map.html')

# 3. API Itinéraire (Sécurisée et Standardisée)
@api_view(['GET']) # Décorateur DRF pour gérer proprement les méthodes
def api_calculate_route(request):
    """
    Endpoint: /api/route/?start=Tanger&end=Agadir
    """
    start_city = request.query_params.get('start') # Convention DRF
    end_city = request.query_params.get('end')

    if not start_city or not end_city:
        return Response({'error': 'Villes de départ et d\'arrivée requises'}, status=400)

    try:
        # Appel de l'algo (Protection contre les crashs)
        distance, path = get_shortest_path(start_city, end_city)

        if distance == float('inf'):
            return Response({'error': 'Aucune route trouvée entre ces villes'}, status=404)

        # Préparation des coordonnées pour Leaflet
        # Note: Leaflet veut [Lat, Lon]. GeoJSON standard est [Lon, Lat].
        path_coordinates = []
        for city in path:
            coord = CITIES_COORDS.get(city)
            if coord:
                path_coordinates.append([coord[1], coord[0]])

        return Response({
            'distance_km': round(distance),
            'chemin': path,
            'path_coordinates': path_coordinates
        })

    except Exception as e:
        # Si utils.py plante, on renvoie l'erreur proprement au lieu de crasher le serveur
        return Response({'error': f"Erreur interne : {str(e)}"}, status=500)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Pour le login
from rest_framework.decorators import api_view             # Pour l'API
from rest_framework.response import Response
from .models import Vehicule
from .serializers import VehiculeSerializer

# 1. La Vue pour la CARTE 
@login_required # permet la redirection vers Login quand on n'est pas connecté
def map_view(request):
    return render(request, 'fleet/map.html')

# 2. La Vue pour l'API
@api_view(['GET'])
def api_vehicules(request):
    vehicules = Vehicule.objects.all()
    serializer = VehiculeSerializer(vehicules, many=True)
    # On renvoie les données au format GeoJSON
    return Response({"type": "FeatureCollection", "features": serializer.data})
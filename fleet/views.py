from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicule
from .serializers import VehiculeSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Vue pour la page HTML (déjà faite hier)
def map_view(request):
    return render(request, 'fleet/map.html')

# NOUVELLE VUE : L'API JSON
@api_view(['GET'])
def api_vehicules(request):
    vehicules = Vehicule.objects.all()
    serializer = VehiculeSerializer(vehicules, many=True)
    return Response({"type": "FeatureCollection", "features": serializer.data})

# Redirige vers le Login si on n'est pas connecté
@login_required 
def map_view(request):
    return render(request, 'fleet/map.html')
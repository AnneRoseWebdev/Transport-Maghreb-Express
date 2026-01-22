from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer # Utilisation de la librairie SIG
from .models import Vehicule

class VehiculeSerializer(GeoFeatureModelSerializer):
    # On garde ton champ calculé intelligent
    diagnostic = serializers.SerializerMethodField()

    class Meta:
        model = Vehicule
        # C'est LA différence : on dit quel champ contient la géométrie
        geo_field = "position_actuelle" 
        
        # On inclut tous les champs nécessaires
        fields = ['id', 'immatriculation', 'statut', 'carburant_niveau', 'kilometrage', 'diagnostic']

    def get_diagnostic(self, obj):
        # On appelle ta méthode intelligente définie dans models.py
        return obj.diagnostic_moteur()
from rest_framework import serializers
from .models import Vehicule


class VehiculeSerializer(serializers.ModelSerializer):
    # On crée un champ spécial qui va contenir le résultat de ton algo
    diagnostic = serializers.SerializerMethodField()

    class Meta:
        model = Vehicule
        # On liste TOUT ce que le JavaScript a besoin de savoir
        fields = ['id', 'immatriculation', 'statut', 'carburant_niveau', 'kilometrage', 'diagnostic', 'position_actuelle']

    def get_diagnostic(self, obj):
        # C'est ici qu'on appelle l'intelligence codée par Anne Rose
        return obj.diagnostic_moteur()
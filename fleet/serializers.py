from rest_framework import serializers
from .models import Vehicule

class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = '__all__' # recupere tous les elements (id, immatriculation, position, etc.)
import os
import django
import random
import json

# Configuration pour utiliser Django hors du serveur
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from fleet.models import Vehicule
from django.contrib.gis.geos import Point

# Liste de villes marocaines pour des coordonnées réalistes
VILLES = [
    (-5.833954, 35.759465), # Tanger
    (-7.589843, 33.573110), # Casablanca
    (-9.603328, 30.419519), # Agadir
    (-6.849813, 34.020882), # Rabat
    (-5.000000, 34.033333), # Fès
]

def generer():
    Vehicule.objects.all().delete() # On vide pour éviter les doublons
    print("Base nettoyée.")
    
    for i in range(1, 51):
        # Position aléatoire autour d'une ville
        ville = random.choice(VILLES)
        lon = ville[0] + random.uniform(-0.5, 0.5)
        lat = ville[1] + random.uniform(-0.5, 0.5)
        
        Vehicule.objects.create(
            immatriculation=f"MAD-{1000+i}-A",
            position_actuelle=Point(lon, lat),
            statut=random.choice(['EN_LIVRAISON', 'GARAGE', 'MAINTENANCE_REQUISE']),
            carburant_niveau=random.randint(10, 100),
            kilometrage=random.randint(0, 15000)
        )
    print(" 50 Véhicules créés avec succès !")

if __name__ == '__main__':
    generer()
from django.core.management.base import BaseCommand
from fleet.models import Vehicule
import random

class Command(BaseCommand):
    help = 'Simule le déplacement et la consommation de la flotte'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Démarrage de la simulation...")
        
        vehicules = Vehicule.objects.all()
        count = 0

        for v in vehicules:
            # 1. Simulation GPS : On déplace le camion légèrement
            # (On ajoute une petite valeur aléatoire à la latitude/longitude)
            lon = v.position_actuelle.x + random.uniform(-0.05, 0.05)
            lat = v.position_actuelle.y + random.uniform(-0.05, 0.05)
            v.position_actuelle = f"POINT({lon} {lat})"

            # 2. Simulation Moteur : Il roule, donc il consomme
            dist = random.uniform(5, 50) # Il a parcouru entre 5 et 50 km
            v.kilometrage += dist
            v.carburant_niveau -= random.uniform(1, 5) # Il perd du fuel

            # Sécurité pour ne pas avoir de carburant négatif
            if v.carburant_niveau < 0:
                v.carburant_niveau = 0
                v.statut = "PANNE_SECHE"
            
            v.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f" Simulation terminée pour {count} véhicules !"))
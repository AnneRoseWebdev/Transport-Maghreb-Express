import time
import random
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from fleet.models import Vehicule, HistoriquePosition

class Command(BaseCommand):
    help = 'Simule le déplacement des camions GPS (Version Avancée)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Démarrage du simulateur GPS Avancé... (CTRL+C pour arrêter)'))

        while True:
            vehicules = Vehicule.objects.all()
            
            for vehicule in vehicules:
                # Initialisation si pas de position
                if not vehicule.position_actuelle:
                    vehicule.position_actuelle = Point(-7.6, 33.5) # Casablanca

                # --- 1. LOGIQUE DE DÉPLACEMENT ---
                x = vehicule.position_actuelle.x
                y = vehicule.position_actuelle.y

                # Déplacement aléatoire léger
                delta_x = random.uniform(-0.02, 0.02) # J'ai augmenté un peu la vitesse pour la démo
                delta_y = random.uniform(-0.02, 0.02)

                new_point = Point(x + delta_x, y + delta_y, srid=4326)
                vehicule.position_actuelle = new_point
                
                # --- 2. LOGIQUE MÉTIER ---
                vehicule.kilometrage += random.uniform(2, 10)
                
                if vehicule.carburant_niveau > 0:
                    vehicule.carburant_niveau -= random.uniform(0.1, 0.5)

                # --- 3. LOGIQUE D'ALERTE ---
                if vehicule.kilometrage > 100000: # J'ai mis 100k pour être cohérent avec l'ancien test
                    vehicule.statut = 'MAINTENANCE_REQUISE'
                elif vehicule.carburant_niveau < 10:
                    vehicule.statut = 'PANNE_ESSENCE'
                else:
                    vehicule.statut = 'EN_LIVRAISON'
                
                # Bonus : Ravitaillement auto pour que la démo ne s'arrête pas
                if vehicule.carburant_niveau <= 0:
                    vehicule.carburant_niveau = 100
                
                vehicule.save()

                # --- 4. ARCHIVAGE HISTORIQUE (Le point fort de ton code) ---
                HistoriquePosition.objects.create(
                    vehicule=vehicule,
                    position=new_point,
                    vitesse=random.uniform(40, 90)
                )

                # Affichage discret
                self.stdout.write(f"🚚 {vehicule.immatriculation}: {vehicule.statut} | {round(vehicule.carburant_niveau)}%")

            # Pause de 3 secondes (bon équilibre pour la démo)
            time.sleep(3)
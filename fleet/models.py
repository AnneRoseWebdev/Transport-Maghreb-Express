from django.contrib.gis.db import models

class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    statut = models.CharField(max_length=20)
    carburant_niveau = models.FloatField(default=100.0) 
    kilometrage = models.FloatField(default=0.0)
    position_actuelle = models.PointField()

    def __str__(self):
        return self.immatriculation

    # === L'ALGORITHME MÉTIER (Jour 4) ===
    def diagnostic_moteur(self):
        """
        Retourne 'CRITIQUE' si < 10% carburant ou > 100 000 km.
        Retourne 'ATTENTION' si < 25% carburant.
        Sinon retourne 'OK'.
        """
        if self.carburant_niveau < 10 or self.kilometrage > 100000:
            return "CRITIQUE"
        elif self.carburant_niveau < 25:
            return "ATTENTION"
        return "OK"
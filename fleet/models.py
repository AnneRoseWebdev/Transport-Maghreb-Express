from django.contrib.gis.db import models

# 1. Le Véhicule
class Vehicule(models.Model):
    STATUT_CHOICES = [
        ('EN_LIVRAISON', 'En Livraison'),
        ('GARAGE', 'Au Garage'),
        ('PANNE', 'En Panne'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    position_actuelle = models.PointField(srid=4326, null=True, blank=True) 
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='GARAGE')
    carburant_niveau = models.FloatField(default=100.0) 
    kilometrage = models.FloatField(default=0.0) # Compteur km total
    
    def __str__(self):
        return self.immatriculation

# 2. Le Trajet 
class Trajet(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    point_depart = models.PointField(srid=4326)
    point_arrivee = models.PointField(srid=4326)
    itineraire_prevu = models.LineStringField(srid=4326, null=True, blank=True)
    date_depart = models.DateTimeField(auto_now_add=True)

# 3. L'Historique
class HistoriquePosition(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    position = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now_add=True)
    vitesse = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-timestamp']
from django.test import TestCase
from django.urls import reverse
from .models import Vehicule

class VehiculeTests(TestCase):
    def setUp(self):
            # On crée un camion virtuel pour le test
            self.camion = Vehicule.objects.create(
                immatriculation="TEST-001",
                statut="GARAGE",
                carburant_niveau=50.0,
                position_actuelle="POINT(-7.6 33.5)" 
            )

    def test_creation_vehicule(self):
        """Vérifie que le camion est bien créé en base"""
        self.assertEqual(self.camion.immatriculation, "TEST-001")
        print("Test Création OK")

    def test_api_access(self):
        """Vérifie que l'API répond bien (Code 200)"""
        response = self.client.get('/api/vehicules/')
        self.assertEqual(response.status_code, 200)
        print("Test API OK")



    def test_algorithme_metier(self):
        """Vérifie que le diagnostic détecte bien une panne sèche"""
        # On crée un camion avec 5% de carburant
        camion_critique = Vehicule.objects.create(
            immatriculation="TEST-CRITIQUE",
            statut="EN_MARCHE",
            carburant_niveau=5.0, # Danger !
            position_actuelle="POINT(0 0)"
        )
        # On demande au modèle son diagnostic
        diag = camion_critique.diagnostic_moteur()
        
        # On vérifie que le système répond bien CRITIQUE
        self.assertEqual(diag, "CRITIQUE")
        print("Test Métier (Algorithme) OK")
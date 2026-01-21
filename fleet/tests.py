from django.test import TestCase
from django.urls import reverse
from .models import Vehicule

class VehiculeTests(TestCase):
    def setUp(self):
        # On crée un camion virtuel pour le test
        self.camion = Vehicule.objects.create(
            immatriculation="TEST-001",
            statut="GARAGE",
            carburant_niveau=50.0
        )

    def test_creation_vehicule(self):
        """Vérifie que le camion est bien créé en base"""
        self.assertEqual(self.camion.immatriculation, "TEST-001")
        print("✅ Test Création OK")

    def test_api_access(self):
        """Vérifie que l'API répond bien (Code 200)"""
        response = self.client.get('/api/vehicules/')
        self.assertEqual(response.status_code, 200)
        print("✅ Test API OK")
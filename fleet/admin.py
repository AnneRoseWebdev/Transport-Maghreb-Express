from django.contrib import admin
# On importe nos modèles depuis le fichier models.py
from .models import Vehicule

# Cette classe sert à configurer l'affichage (colonnes, filtres...)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'statut', 'carburant_niveau', 'kilometrage') # Les colonnes visibles
    list_filter = ('statut',) # Ajoute un filtre latéral pour trier par statut
    search_fields = ('immatriculation',) # Ajoute une barre de recherche

# La ligne magique qui fait apparaître le menu dans l'interface
admin.site.register(Vehicule, VehiculeAdmin)
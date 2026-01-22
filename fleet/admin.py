from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.html import format_html
from .models import Vehicule, Trajet, HistoriquePosition

@admin.register(Vehicule)
class VehiculeAdmin(GISModelAdmin):
    list_display = ('immatriculation', 'statut_badge', 'jauge_carburant', 'etat_sante', 'kilometrage')
    list_filter = ('statut',)
    search_fields = ('immatriculation',)

    gis_widget_kwargs = {
        'attrs': {
            'default_lon': -6.0,
            'default_lat': 32.0,
            'default_zoom': 6,
        }
    }

    # 1. Badge de statut coloré
    def statut_badge(self, obj):
        color = '#76C893' # Vert par défaut
        if obj.statut in ['PANNE', 'GARAGE', 'PANNE_ESSENCE', 'MAINTENANCE_REQUISE']:
            color = '#D90429' # Rouge
        elif obj.statut == 'EN_LIVRAISON':
            color = '#FF9F1C' # Orange
        
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px; font-weight:bold;">{}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"

    # 2. Jauge de carburant visuelle
    def jauge_carburant(self, obj):
        color = '#76C893' # Vert
        if obj.carburant_niveau < 20: color = '#D90429' # Rouge
        elif obj.carburant_niveau < 50: color = '#FFB703' # Orange
        
        return format_html(
            '<div style="width:100px; background:#e0e0e0; border-radius:5px;">'
            '<div style="width:{}%; background:{}; height:10px; border-radius:5px;"></div>'
            '</div>',
            obj.carburant_niveau, color
        )
    
    # 3. Colonne Diagnostic (C'EST ICI QUE C'ÉTAIT CASSÉ)
    def etat_sante(self, obj):
        diag = obj.diagnostic_moteur()
        
        if diag == "CRITIQUE":
            # CORRECTION : On passe le texte "CRITIQUE" comme argument {}
            return format_html(
                '<span style="color:#D90429; font-weight:bold;">{}</span>',
                "⚠️ CRITIQUE"
            )
        elif diag == "ATTENTION":
            return format_html(
                '<span style="color:#FF9F1C; font-weight:bold;">{}</span>',
                "⚠️ ATTENTION"
            )
        
        return format_html(
            '<span style="color:#76C893; font-weight:bold;">{}</span>',
            "✅ OK"
        )

# --- ENREGISTREMENT DES AUTRES MODÈLES ---

@admin.register(Trajet)
class TrajetAdmin(GISModelAdmin):
    list_display = ('vehicule', 'date_depart')
    gis_widget_kwargs = {'attrs': {'default_lon': -6.0, 'default_lat': 32.0, 'default_zoom': 6}}

@admin.register(HistoriquePosition)
class HistoriqueAdmin(GISModelAdmin):
    list_display = ('vehicule', 'timestamp', 'vitesse')
    list_filter = ('vehicule', 'timestamp')
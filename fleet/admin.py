from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicule

class VehiculeAdmin(admin.ModelAdmin):
    # On ajoute nos nouvelles colonnes "intelligentes"
    list_display = ('immatriculation', 'statut_badge', 'jauge_carburant', 'etat_sante', 'kilometrage')
    list_filter = ('statut',)
    search_fields = ('immatriculation',)

    # 1. Badge de statut coloré
    def statut_badge(self, obj):
        color = 'green'
        if obj.statut in ['PANNE', 'GARAGE', 'PANNE_SECHE']:
            color = 'red'
        elif obj.statut == 'EN_LIVRAISON':
            color = 'orange'
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            color, obj.statut
        )
    statut_badge.short_description = "Statut"

    # 2. Jauge de carburant visuelle
    def jauge_carburant(self, obj):
        color = '#76C893' # Vert
        if obj.carburant_niveau < 20: color = '#D90429' # Rouge
        elif obj.carburant_niveau < 50: color = '#FFB703' # Orange
        
        return format_html(
            '<div style="width:100px; background:#eee; border-radius:5px;">'
            '<div style="width:{}%; background:{}; height:10px; border-radius:5px;"></div>'
            '</div>',
            obj.carburant_niveau, color
        )
    
   # 3. Colonne Diagnostic
    def etat_sante(self, obj):
        diag = obj.diagnostic_moteur()
        if diag == "CRITIQUE":
            # On met le texte dans le format_html via {} pour éviter l'erreur
            return format_html(
                '<span style="color:red; font-weight:bold;">{}</span>', 
                "⚠️ CRITIQUE"
            )
        elif diag == "ATTENTION":
            return format_html(
                '<span style="color:orange; font-weight:bold;">{}</span>', 
                "⚠️ ATTENTION"
            )
        return "✅ OK"

admin.site.register(Vehicule, VehiculeAdmin)
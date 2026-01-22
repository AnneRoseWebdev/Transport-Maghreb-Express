## Travail Réaliser par :
   -Frank Loic KENFACK
   -Anne Rose NGALANI WANSI
   -Abid RAKHIS

# 🚛 LogiTrack - Transport Maghreb Express

**Solution de gestion de flotte intelligente (FMS) avec suivi temps réel, optimisation algorithmique et maintenance prédictive.**

---

## 📝 Description du Projet
Ce projet a été développé dans le cadre d'un Hackathon de 5 jours pour répondre à la problématique de **Transport Maghreb Express**. L'objectif est de réduire les coûts opérationnels de 20% et d'améliorer la fiabilité des livraisons grâce à une plateforme centralisée.

L'application permet de visualiser une flotte de 50 camions en temps réel, de calculer des itinéraires optimaux (Dijkstra) et d'alerter les superviseurs en cas d'anomalies mécaniques.

---

## Fonctionnalités Clés

###  1. Cartographie & Temps Réel
* **Visualisation Live :** Affichage des camions sur une carte interactive (Leaflet + OpenStreetMap).
* **Mise à jour fluide :** Rafraîchissement automatique des positions toutes les 2 secondes sans rechargement de page (AJAX/Fetch).
* **Flux GeoJSON :** Utilisation du standard GeoJSON via `djangorestframework-gis` pour une interopérabilité maximale.

###  2. Algorithmes & Intelligence
* **Optimisation de Trajets (Dijkstra) :** Moteur de calcul d'itinéraire "maison" (codé en Python) trouvant le chemin le plus court entre les grandes villes du Maroc.
* **Maintenance Prédictive :** Algorithme détectant automatiquement les statuts critiques (Surchauffe, Panne Essence, Révision nécessaire) basé sur le kilométrage et le niveau de carburant.

###  3. Outils Métier & Décisionnel
* **Calculateur ROI :** Module d'estimation des économies financières en temps réel basé sur la flotte active.
* **Dashboard Admin Avancé :** Interface d'administration GeoDjango avec :
    * Carte interactive pour l'édition des positions.
    * Jauges visuelles de carburant.
    * Badges de statut colorés.
    * Filtres de recherche multicritères.

###  4. Sécurité
* **Authentification :** Système de Login/Logout sécurisé pour les superviseurs.
* **Protection API :** Structure Django Rest Framework robuste.

---

##  Stack Technique

* **Backend :** Python 3.10+, Django 5.0.
* **Base de Données Spatiale :** PostgreSQL + Extension **PostGIS**.
* **API :** Django REST Framework + `djangorestframework-gis`.
* **Frontend :** JavaScript , Leaflet.js, CSS3 (Animations Custom).
* **Simulation :** Script Python stochastique (Génération de trafic réaliste).

---

##  Guide d'Installation

### 1. Pré-requis
* Python installé.
* PostgreSQL installé avec PostGIS activé.
* Créer une base de données nommée `maghreb_express`.

### 2. Installation des dépendances
# Activer l'environnement virtuel
venv\Scripts\activate sur Windows

# Installer les paquets requis
pip install -r requirements.txt


#Migrations & Configuration
# Appliquer les schémas de base de données
python manage.py makemigrations
python manage.py migrate

# Créer un administrateur (pour l'accès Superviseur)
python manage.py createsuperuser

#Pour générer les 50 premiers camions
# Dans le terminal, exécuter le script de peuplement 
# Ou laisser le simulateur créer les positions par défaut.
python generate_data.py

###Lancer la Démo

## Ouvrir le premier Terminal  : Le Serveur Web
python manage.py runserver

## Ouvrir un deuxieme Terminal : Le Simulateur de Trafic
# Ce script fait "vivre" la flotte en déplaçant les camions et en consommant du carburant
python manage.py simulate_fleet 

###Guide d'Utilisation

## Accès Superviseur :
  -Rendez-vous sur http://127.0.0.1:8000/accounts/login/
  -Connectez-vous avec vos identifiants.

## Dashboard Tracking :
  -Une fois connecté, vous êtes redirigé vers la carte (/map/).
  -Tracer une route : Utilisez le panneau gauche, sélectionnez "Tanger" -> "Agadir" et cliquez sur "Tracer la route".
  -Voir le ROI : Cliquez sur le bouton orange "Calculer Économies" en bas à droite.

## Administration Technique :
  -Accès via http://127.0.0.1:8000/admin/
  -Permet de modifier manuellement un véhicule, voir l'historique des positions et gérer les utilisateurs.

### Mode de fonctionnement de l'API
  -GET /api/vehicules/ : Renvoie la liste complète de la flotte en format GeoJSON.  
  -GET /api/vehicules/{id}/ : Détails d'un véhicule spécifique.
  -GET /api/route/?start=VilleA&end=VilleB : Calcule et renvoie le chemin optimal (Algorithme Dijkstra).
# Transport-Maghreb-Express
Projet de gestion de transport

Crée l'environnement virtuel : python -m venv venv.

Active l'environnement : venv\Scripts\activate

Installer Django : pip install django djangorestframework djangorestframework-gis psycopg2-binary.

Lancement du projet : django-admin startproject backend . 
   - le point a la fin de la commande permet de ne pas crée des dossiers inutiles

Création du coeur de notre application : python manage.py startapp fleet

créer un administrateur pour notre interface : python manage.py createsuperuser

Commande pour lancer notre serveur : python manage.py runserver

ouvrir le navigateur et utiliser le lien : http://127.0.0.1:8000/admin/ pour ce connecter a l'espace administrateur
   . Nom d'utilisateur : admin
   . Mot de passe : password123


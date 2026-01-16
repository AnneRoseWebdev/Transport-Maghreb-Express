-- 1. Nettoyage (Attention, supprime tout !)
DROP DATABASE IF EXISTS maghreb_express;

-- 2. Création de la base
CREATE DATABASE maghreb_express;

-- 3. Connexion (si exécuté en ligne de commande, sinon changer de base dans pgAdmin)
\c maghreb_express;

-- 4. Activation PostGIS (OBLIGATOIRE)
CREATE EXTENSION postgis;
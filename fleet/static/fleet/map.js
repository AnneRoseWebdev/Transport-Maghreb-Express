document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialisation de la carte (Centrée sur le Maroc)
    var map = L.map('map').setView([31.7917, -7.0926], 6);

    // 2. Ajout du fond de carte
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 3. Fonction pour charger les véhicules
    function chargerVehicules() {
        fetch('/api/vehicules/') 
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erreur réseau ou API non accessible");
                }
                return response.json();
            })
            .then(data => {
                console.log("Données reçues :", data); 

                // --- C'est ICI que tout change ---
                // On boucle sur chaque véhicule
                // Note: Selon ton API, 'data' est peut-être directement la liste, ou data.features
                // Si ton API renvoie une liste directe, utilise 'data.forEach'
                // Si ton API renvoie du GeoJSON, utilise 'data.features.forEach'
                // Je garde ta logique 'data.features' (si ça plante, essaie juste 'data.forEach')
                var listeVehicules = data.features || data; 

                listeVehicules.forEach(vehicule => {
                    // Récupération des coordonnées (Ta méthode actuelle)
                    // Sécurité : on vérifie si position_actuelle est un objet ou une string
                    var lat, lon;
                    
                    if (vehicule.position_actuelle && vehicule.position_actuelle.coordinates) {
                        lat = vehicule.position_actuelle.coordinates[1];
                        lon = vehicule.position_actuelle.coordinates[0];
                    } else {
                        // Cas de secours si le format change
                        console.warn("Format de position inconnu pour", vehicule.immatriculation);
                        return; // On passe au suivant
                    }

                    // Récupération des nouvelles infos "Intelligentes"
                    var immat = vehicule.immatriculation;
                    var statut = vehicule.statut;
                    var carburant = vehicule.carburant_niveau;
                    var diagnostic = vehicule.diagnostic; // Vient de ton Serializer
                    var km = vehicule.kilometrage;

                    // Choix de la couleur du badge Diagnostic
                    var couleurDiag = 'green';
                    if (diagnostic === 'CRITIQUE') couleurDiag = 'red';
                    else if (diagnostic === 'ATTENTION') couleurDiag = 'orange';

                    // Choix de la couleur de la jauge carburant
                    var couleurJauge = '#76C893'; // Vert
                    if (carburant < 20) couleurJauge = 'red';
                    else if (carburant < 50) couleurJauge = 'orange';

                    // Création du HTML de la Popup (Design Pro)
                    var popupContent = `
                        <div style="font-family: 'Segoe UI', sans-serif; min-width: 160px;">
                            <h3 style="margin:0 0 5px 0; color:#163E50; border-bottom:1px solid #ddd; padding-bottom:5px;">
                                🚛 ${immat}
                            </h3>
                            
                            <div style="margin-bottom:5px; font-size:13px;">
                                <strong>Statut :</strong> ${statut}<br>
                                <strong>Km :</strong> ${Math.round(km)} km
                            </div>
                            
                            <div style="background:#eee; width:100%; height:10px; border-radius:5px; border:1px solid #ccc;">
                                <div style="background:${couleurJauge}; width:${carburant}%; height:100%; border-radius:5px;"></div>
                            </div>
                            <div style="text-align:right; font-size:11px; margin-bottom:8px;">Fuel: ${Math.round(carburant)}%</div>

                            <div style="background:${couleurDiag}; color:white; text-align:center; padding:4px; border-radius:4px; font-weight:bold; font-size:12px;">
                                DIAGNOSTIC : ${diagnostic}
                            </div>
                        </div>
                    `;

                    // Ajout du marqueur et de la popup
                    var marker = L.marker([lat, lon]).addTo(map);
                    marker.bindPopup(popupContent);
                });
            })
            .catch(error => {
                console.error("Erreur lors du chargement :", error);
            });
    }

    // 4. Lancement
    chargerVehicules();
});
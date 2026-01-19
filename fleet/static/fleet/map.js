document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Initialisation de la carte (Centrée sur le Maroc)
    // Coordonnées : [Latitude, Longitude], Zoom : 6
    var map = L.map('map').setView([31.7917, -7.0926], 6);

    // 2. Ajout du fond de carte (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 3. Fonction pour charger les véhicules depuis l'API (Le lien avec le Backend)
    function chargerVehicules() {
        fetch('/api/vehicules/')  // <-- C'est ici qu'on appelle ton URL Django
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erreur réseau ou API non accessible");
                }
                return response.json();
            })
            .then(data => {
                // "data" contient maintenant le JSON de tes 50 camions
                console.log("Données reçues :", data); 

                // On boucle sur chaque véhicule pour l'ajouter à la carte
                data.features.forEach(vehicule => {
                    var lat = vehicule.position_actuelle.coordinates[1]; // Attention: PostGIS inverse parfois Lat/Lon
                    var lon = vehicule.position_actuelle.coordinates[0];
                    var immat = vehicule.immatriculation;
                    var statut = vehicule.statut;

                    // Ajout du marqueur
                    var marker = L.marker([lat, lon]).addTo(map);
                    
                    // Ajout d'une popup (bulle d'info au clic)
                    marker.bindPopup(`
                        <b>Camion : ${immat}</b><br>
                        Statut : ${statut}<br>
                        <button onclick="alert('Détails du ${immat}')">Voir détails</button>
                    `);
                });
            })
            .catch(error => {
                console.error("Erreur lors du chargement des camions :", error);
                // Si l'API ne marche pas encore, on peut décommenter ceci pour tester :
                alert("Impossible de charger les camions. Vérifiez que le serveur tourne.");
            });
    }

    // 4. On lance le chargement
    chargerVehicules();

});
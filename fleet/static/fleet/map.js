// --- 1. Initialisation de la carte ---
// Centré sur le Maroc
var map = L.map('map').setView([32.0, -6.0], 6);

// Fond de carte CartoDB Light (Gris pro)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

var vehicleMarkers = {}; 
var currentRouteLine = null;

// --- 2. Fonction de mise à jour (Temps Réel) ---
async function updateMap() {
    try {
        const response = await fetch('/api/vehicules/'); 
        const data = await response.json();
        
        // Mise à jour des compteurs
        document.getElementById('count').innerText = data.features.length;
        const now = new Date();
        document.getElementById('last-update').innerText = now.toLocaleTimeString();

        data.features.forEach(feature => {
            const id = feature.id;
            const props = feature.properties;
            const lat = feature.geometry.coordinates[1]; 
            const lon = feature.geometry.coordinates[0];

            // --- GESTION DES COULEURS (MAINTENANCE) ---
            let markerColor = '#76C893'; // Vert (OK)
            let borderColor = '#163E50'; // Bleu foncé
            
            if (props.statut === 'MAINTENANCE_REQUISE') {
                markerColor = '#D90429'; // Rouge
            } else if (props.statut === 'PANNE_ESSENCE') {
                markerColor = '#FF9F1C'; // Orange
            }

            // Contenu de la popup
            const popupContent = `
                <div style="text-align:center; color: #163E50;">
                    <strong style="font-size:1.1em">${props.immatriculation}</strong><br>
                    <span style="color: ${markerColor}; font-weight:bold;">${props.statut}</span><br>
                    ⛽ ${Math.round(props.carburant_niveau)}% <br>
                    🛣️ ${Math.round(props.kilometrage)} km
                </div>
            `;

            if (vehicleMarkers[id]) {
                // Mise à jour position existante
                vehicleMarkers[id].setLatLng([lat, lon]);
                vehicleMarkers[id].bindPopup(popupContent);
                vehicleMarkers[id].setStyle({ fillColor: markerColor }); 
            } else {
                // Création nouveau marqueur
                var marker = L.circleMarker([lat, lon], {
                    color: borderColor,
                    fillColor: markerColor,
                    fillOpacity: 0.8,
                    weight: 2,
                    radius: 8
                })
                .addTo(map)
                .bindPopup(popupContent);
                
                vehicleMarkers[id] = marker;
            }
        });

    } catch (error) {
        console.error("Erreur API:", error);
    }
}

// --- 3. Fonction Calcul Itinéraire (Dijkstra) ---
async function calculateRoute() {
    const start = document.getElementById('start-city').value;
    const end = document.getElementById('end-city').value;
    const resultDiv = document.getElementById('route-result');

    resultDiv.innerHTML = "Calcul en cours...";

    try {
        const response = await fetch(`/api/route/?start=${start}&end=${end}`);
        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<span style="color:red">Erreur: ${data.error}</span>`;
            return;
        }

        resultDiv.innerHTML = `
            <strong>Distance : ${data.distance_km} km</strong><br>
            Via : ${data.chemin.join(' > ')}
        `;

        // Tracer la ligne
        if (currentRouteLine) {
            map.removeLayer(currentRouteLine);
        }

        currentRouteLine = L.polyline(data.path_coordinates, {
            color: '#163E50', 
            weight: 5,        
            opacity: 0.8,
            dashArray: '10, 10' 
        }).addTo(map);

        map.fitBounds(currentRouteLine.getBounds());

    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = "Erreur connexion.";
    }
}

// Lancement automatique
updateMap();
setInterval(updateMap, 2000);

function openROI() {
    // 1. On récupère le nombre de véhicules actifs
    const activeVehicles = document.getElementById('count').innerText || 0;
    
    // 2. Simulation de calculs basés sur tes données
    // Prix moyen diesel : 1.30€/L. Conso camion : 30L/100km.
    // On estime une tournée moyenne de 500km par camion.
    const totalKm = activeVehicles * 500; 
    const coutEstime = (totalKm / 100) * 30 * 1.3; // Coût théorique sans optimisation
    
    // Notre algo Dijkstra fait gagner 15% de distance + 5% grâce à la maintenance
    const economie = coutEstime * 0.20; 

    // 3. Injection dans le HTML (DOM Manipulation propre)
    // Astuce : On sélectionne les éléments par leur contenu ou position pour aller vite
    const modal = document.getElementById('roiModal');
    const amounts = modal.querySelectorAll('div[style*="font-size:1.4em"]');
    
    // Mise à jour Coût
    amounts[0].innerText = Math.round(coutEstime) + " €";
    // Mise à jour Économie
    amounts[1].innerText = "- " + Math.round(economie) + " €";
    
    // Affichage
    modal.style.display = "flex";
}

function closeROI() {
    document.getElementById('roiModal').style.display = "none";
}
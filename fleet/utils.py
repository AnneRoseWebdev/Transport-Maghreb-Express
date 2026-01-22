import heapq

# 1. La Carte Simplifiée (Graphe)
# Les distances sont approximatives (en km)
GRAPH = {
    'Tanger': {'Rabat': 250, 'Fes': 300},
    'Rabat': {'Tanger': 250, 'Casablanca': 90, 'Fes': 200},
    'Casablanca': {'Rabat': 90, 'Marrakech': 240, 'El Jadida': 100},
    'Fes': {'Tanger': 300, 'Rabat': 200, 'Oujda': 350, 'Marrakech': 530},
    'Marrakech': {'Casablanca': 240, 'Fes': 530, 'Agadir': 250},
    'Agadir': {'Marrakech': 250, 'Essaouira': 175},
    'El Jadida': {'Casablanca': 100, 'Safi': 150},
    'Safi': {'El Jadida': 150, 'Essaouira': 130},
    'Essaouira': {'Safi': 130, 'Agadir': 175},
    'Oujda': {'Fes': 350}
}

# 2. Les Coordonnées GPS des villes (Pour tracer la ligne sur la carte)
CITIES_COORDS = {
    'Tanger': [-5.83, 35.75],
    'Rabat': [-6.84, 34.02],
    'Casablanca': [-7.58, 33.57],
    'Fes': [-5.00, 34.03],
    'Marrakech': [-7.98, 31.62],
    'Agadir': [-9.60, 30.42],
    'El Jadida': [-8.50, 33.23],
    'Safi': [-9.22, 32.29],
    'Essaouira': [-9.77, 31.50],
    'Oujda': [-1.90, 34.68]
}

# 3. L'Algorithme de Dijkstra (Le cœur du sujet)
def get_shortest_path(start_node, end_node):
    """
    Retourne (distance_totale, liste_des_villes)
    """
    queue = [(0, start_node, [])] # (Coût, Noeud Actuel, Chemin)
    seen = set()
    min_dist = {start_node: 0}

    while queue:
        (cost, v1, path) = heapq.heappop(queue)

        if v1 in seen:
            continue

        seen.add(v1)
        path = path + [v1]

        if v1 == end_node:
            return (cost, path)

        for v2, dist in GRAPH.get(v1, {}).items():
            if v2 in seen:
                continue
            prev = min_dist.get(v2, None)
            next_cost = cost + dist
            if prev is None or next_cost < prev:
                min_dist[v2] = next_cost
                heapq.heappush(queue, (next_cost, v2, path))

    return float("inf"), []
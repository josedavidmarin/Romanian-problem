#Jose David Marin Giraldo - C.c: 1004681831 - 18/09/2024
#Rumanian Problem - Algoritmos de Búsqueda - UCS y A*

import heapq #librería que proporciona una estructura de datos de cola de prioridad. En nuestro caso, se usa para mantener la frontera (los nodos por explorar) ordenada por el costo más bajo.
import math #Se utiliza para calcular la distancia euclidiana (heurística en A*).
import matplotlib.pyplot as plt #Es la librería que permite dibujar y mostrar el mapa con las rutas de los algoritmos.

# Define las conexiones entre las ciudades. Cada ciudad tiene un diccionario de ciudades vecinas y las distancias a ellas.
graph = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Dobreta': 75},
    'Dobreta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Dobreta': 120, 'Pitesti': 138, 'Rimnicu_Vilcea': 146},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu_Vilcea': 80},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu_Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Pitesti': {'Rimnicu_Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Es un diccionario que asocia cada ciudad con sus coordenadas en el plano para facilitar la visualización.
coordinates = {
    'Arad': (29, 192), 'Bucharest': (268, 55), 'Craiova': (163, 22),
    'Dobreta': (91, 32), 'Eforie': (420, 28), 'Fagaras': (208, 157),
    'Giurgiu': (264, 8), 'Hirsova': (396, 74), 'Iasi': (347, 204),
    'Lugoj': (91, 98), 'Mehadia': (93, 65), 'Neamt': (290, 229),
    'Oradea': (62, 258), 'Pitesti': (220, 88), 'Rimnicu_Vilcea': (147, 124),
    'Sibiu': (126, 164), 'Timisoara': (32, 124), 'Urziceni': (333, 74),
    'Vaslui': (376, 153), 'Zerind': (44, 225)
}

# Algoritmo de búsqueda por Costo Uniforme (UCS)
def uniform_cost_search(graph, start, goal):
    frontier = [(0, start, [])] #Inicia la frontera (cola de prioridad). Aquí se almacenan tuplas con el formato (costo_actual, ciudad_actual, ruta_actual). Inicia con la ciudad de partida, un costo de 0, y una ruta vacía.
    visited = set() #Este conjunto almacenará las ciudades que ya fueron visitadas para evitar repetirlas
    
    while frontier:
        cost, city, path = heapq.heappop(frontier) #Se extrae la ciudad con el menor costo acumulado de la frontera. Esto es gracias a que la frontera es una cola de prioridad (usando heapq).
        
        if city in visited:
            continue
        
        path = path + [city]
        
        if city == goal:
            return path, cost
        
        visited.add(city)
        
        for neighbor, distance in graph[city].items(): #Itera sobre los vecinos de la ciudad actual y las distancias hacia ellos.
            if neighbor not in visited:
                heapq.heappush(frontier, (cost + distance, neighbor, path)) #Añade a la frontera el vecino con el nuevo costo acumulado y la ruta actualizada.
    
    return None, float('inf')

# Calcula la distancia euclidiana entre la ciudad actual y Bucarest como una aproximación (heurística).
def heuristic(city, goal='Bucharest'):
    x1, y1 = coordinates[city]
    x2, y2 = coordinates[goal]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star_search(graph, start, goal):
    frontier = [(0, start, [])]
    visited = set()
    g_costs = {start: 0} #Este diccionario almacenará los costos acumulados desde la ciudad de partida hasta cada ciudad
    
    while frontier:
        cost, city, path = heapq.heappop(frontier)
        
        if city in visited:
            continue
        
        path = path + [city]
        
        if city == goal:
            return path, cost
        
        visited.add(city)
        
        for neighbor, distance in graph[city].items():
            new_cost = g_costs[city] + distance
            if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, path)) # Añade el vecino a la frontera con su prioridad calculada.
    
    return None, float('inf')

# Función para graficar el mapa con las rutas
def plot_map(path_ucs, path_a_star):
    fig, ax = plt.subplots()
    
    for city, neighbors in graph.items():
        x, y = coordinates[city]
        ax.scatter(x, y, color='red')
        ax.text(x, y, city, fontsize=10)
        
        for neighbor in neighbors:
            x2, y2 = coordinates[neighbor]
            ax.plot([x, x2], [y, y2], color='gray')
    
    for i in range(len(path_ucs) - 1):
        x1, y1 = coordinates[path_ucs[i]]
        x2, y2 = coordinates[path_ucs[i+1]]
        ax.plot([x1, x2], [y1, y2], color='blue', linewidth=2)
    
    for i in range(len(path_a_star) - 1):
        x1, y1 = coordinates[path_a_star[i]]
        x2, y2 = coordinates[path_a_star[i+1]]
        ax.plot([x1, x2], [y1, y2], color='green', linewidth=2)
    
    plt.show()

# Ejecutar y visualizar
if __name__ == '__main__':
    # Ejecutar UCS y A*
    path_ucs, cost_ucs = uniform_cost_search(graph, 'Arad', 'Bucharest')
    path_a_star, cost_a_star = a_star_search(graph, 'Arad', 'Bucharest')

    # Mostrar los resultados
    print(f"Ruta UCS: {path_ucs}, Costo: {cost_ucs}")
    print(f"Ruta A*: {path_a_star}, Costo: {cost_a_star}")
    
    # Dibujar el mapa
    plot_map(path_ucs, path_a_star)

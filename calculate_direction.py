from queue import PriorityQueue
import numpy as np
import numpy as np
import numpy as np
import networkx as nx

def calculate_direction(snake_position, food_position, previous_move, snake_body):
    print(snake_body)
    # Obtener la posición de la cabeza de la serpiente y la comida
    x1, y1 = snake_position
    x2, y2 = food_position
    board_width=17
    board_height=15
    # Calcular la diferencia entre las posiciones
    dx, dy = x2 - x1, y2 - y1

    # Seleccionar la dirección con la mayor diferencia absoluta
    if abs(dx) > abs(dy):
        if dx > 0:
            if (x1 + 1, y1) not in snake_body and x1 + 1 < board_width:
                return 'right'
            elif (x1, y1 + 1) not in snake_body and y1 + 1 < board_height:
                return 'down'
            elif (x1, y1 - 1) not in snake_body and y1 - 1 >= 0:
                return 'up'
            else:
                return 'left'
        else:
            if (x1 - 1, y1) not in snake_body and x1 - 1 >= 0:
                return 'left'
            elif (x1, y1 + 1) not in snake_body and y1 + 1 < board_height:
                return 'down'
            elif (x1, y1 - 1) not in snake_body and y1 - 1 >= 0:
                return 'up'
            else:
                return 'right'
    else:
        if dy > 0:
            if (x1, y1 + 1) not in snake_body and y1 + 1 < board_height:
                return 'down'
            elif (x1 + 1, y1) not in snake_body and x1 + 1 < board_width:
                return 'right'
            elif (x1 - 1, y1) not in snake_body and x1 - 1 >= 0:
                return 'left'
            else:
                return 'up'
        else:
            if (x1, y1 - 1) not in snake_body and y1 - 1 >= 0:
                return 'up'
            elif (x1 + 1, y1) not in snake_body and x1 + 1 < board_width:
                return 'right'
            elif (x1 - 1, y1) not in snake_body and x1 - 1 >= 0:
                return 'left'
            else:
                return 'down'

def shortest_path(graph, start, end):
    if not graph.has_node(start) or not graph.has_node(end):
        return None
    try:
        return nx.shortest_path(graph, start, end)
    except nx.NetworkXNoPath:
        return None


def a_star(graph, start, goal):
    # Creamos una cola de prioridad y agregamos el nodo inicial con una prioridad de 0
    queue = PriorityQueue()
    queue.put((0, start))
    
    # Diccionario que almacena los nodos visitados y su predecesor
    visited = {start: None}
    
    # Diccionario que almacena los costos desde el inicio hasta cada nodo
    g_score = {start: 0}
    
    # Loop principal del algoritmo
    while not queue.empty():
        # Extraemos el nodo con menor costo
        current_cost, current_node = queue.get()
        
        # Si llegamos al nodo objetivo, construimos y devolvemos el camino
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = visited[current_node]
            return list(reversed(path))
        
        # Expandimos el nodo actual y revisamos sus vecinos
        for neighbor, weight in graph[current_node].items():
            # Si el vecino no es transitble, lo ignoramos
            if weight == 0:
                continue
            
            # Calculamos el costo desde el inicio hasta el vecino a través del nodo actual
            tentative_g_score = g_score[current_node] + weight
            
            # Si el vecino ya ha sido visitado y el costo desde el inicio es menor que el calculado
            # anteriormente, lo ignoramos
            if neighbor in g_score and tentative_g_score >= g_score[neighbor]:
                continue
            
            # Si el vecino no ha sido visitado o el costo desde el inicio es menor que el calculado
            # anteriormente, lo agregamos a la cola de prioridad y actualizamos la información
            visited[neighbor] = current_node
            g_score[neighbor] = tentative_g_score
            f_score = tentative_g_score + heuristic(neighbor, goal)
            queue.put((f_score, neighbor))
    
    # Si no se encuentra un camino, se devuelve None
    return None
def heuristic(a, b):
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

def move(previous_move, path, start):
    print(path)
    for node in path[1:]:
    # Calcular la dirección en la que la serpiente debe moverse para seguir el camino
        x, y = node
        dx = x - start[0]
        dy = y - start[1]
        start = node
        
        # Enviar la tecla de flecha correspondiente para mover la serpiente en la dirección adecuada
        if dx == 1 and previous_move!="left":
            previous_move="right"
        elif dx == -1 and previous_move!="right":
            previous_move="left"
        elif dy == 1 and previous_move!="up":
            previous_move="down"
        elif dy == -1 and  previous_move!="down":
            previous_move="up"
        print(previous_move)
        print(node)
    return(previous_move)

def next_move(current_position, path):
    print(path)
    if not path or current_position not in path:
        return None

    current_index = path.index(current_position)
    
    if current_index + 1 >= len(path):
        return None

    next_position = path[current_index + 1]
    row_diff = next_position[0] - current_position[0]
    col_diff = next_position[1] - current_position[1]

    if col_diff == 1:
        return "down"
    elif col_diff == -1:
        return "up"
    elif row_diff == 1:
        return "right"
    elif row_diff == -1:
        return "left"
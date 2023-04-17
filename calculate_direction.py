from queue import PriorityQueue
import numpy as np
import numpy as np
import numpy as np
import networkx as nx
import heapq

def calculate_direction(snake_position, food_position, previous_move, snake_body):
    #print(snake_body)
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
    #Read nodes and neighbors
    '''
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        print(f"Nodo: {node} -> Vecinos: {neighbors}")
    '''
    if not graph.has_node(start) or not graph.has_node(end):
        return None

    try:
        path = nx.shortest_path(graph, start, end)
    except nx.NetworkXNoPath:
        return None

    moves = {}
    for i in range(len(path) - 1):
        current_position = path[i]
        next_position = path[i + 1]
        col_diff = next_position[0] - current_position[0]
        row_diff = next_position[1] - current_position[1]

        if row_diff == 1:
            move = "down"
        elif row_diff == -1:
            move = "up"
        elif col_diff == 1:
            move = "right"
        elif col_diff == -1:
            move = "left"

        moves[current_position] = move

    moves[path[-1]] = "goal"
    return moves


def a_star(graph, start, goal):
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + manhattan_distance(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    path_dict = {}
    if goal in came_from:
        # Invertir las claves y valores en el diccionario 'came_from'
        came_from_reversed = {v: k for k, v in came_from.items() if v is not None}

        node = start
        while node != goal:
            next_node = came_from_reversed[node]
            if next_node[0] < node[0]:
                direction = "up"
            elif next_node[0] > node[0]:
                direction = "down"
            elif next_node[1] < node[1]:
                direction = "left"
            else:
                direction = "right"
            path_dict[node] = direction
            node = next_node

    return path_dict

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
    if current_position !="goal"  :
        return path.get(current_position)
    return
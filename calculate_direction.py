from queue import PriorityQueue
import numpy as np
import numpy as np
import numpy as np
import networkx as nx
import heapq


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


def next_move(current_position, path):
    #sprint(path)
    if not path or current_position not in path:
        return None
    if current_position !="goal"  :
        return path.get(current_position)
    return
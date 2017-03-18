# Fichier 1 __init__.py que tu renommeras a DAG.py

# Fichier 2 INF4705_TP2.py ou whatever

from DAG import DAG # Importe la classe DAG du module DAG
import os
import sys # pour avoir acces aux arguments de ligne de commande
import numpy as np # pip install numpy
from collections import deque


""" On avait un fichier python dans le TP1 que tu peux regarder pour savoir comment ouvrir des fichiers avec python.  Commence par hardcoder un path, laisse faire les "command line arguments" pour apres que tu aies teste la creation d'un graphe. """

def make_graph(filename):
    """ Returns a DAG created with a filename """

    # 0) Create a dag:
    graph = DAG()

    # 0.1) Open a file
    file = open(filename, "r")

    # 1) Get number of edges and number of nodes
    line = file.readline().split()
    n_nodes = int(line[0])
    n_edges = int(line[1])
    graph.removed = np.zeros((n_nodes)) # Cree un numpy array
    graph.active_nodes = n_nodes

    # 2) Add all the nodes
    for i in range(n_nodes):
    	graph.add_node(i)

    # 3) Add all the edges
    for i in range(n_edges):
    	line = file.readline().split()
        graph.add_edge(int(line[0]), int(line[1]))

    return graph

def lazy_remove(graph, node):
    if graph.removed[node] == False:
        return

    graph.removed[node] = True
    graph.active_nodes -= 1

def lazy_add(graph, node):
    if graph.removed[node] == True:
        return

    graph.removed[node] = False
    graph.active_nodes += 1

def lazy_empty(graph):
    if graph.active_nodes == 0:
        return True
    else:
        return False

def is_active(graph, node):
    return not graph.removed[node]

def lazy_in_degree(graph, node):
    """ Calculates the degree of a node while taking into
    account the nodes that have been lazy-removed """
    in_degree = 0
    for n in graph.predecessors(node):
        if is_active(graph, node):
            in_degree += 1
    return in_degree

def lazy_in_degree_0(graph):
    """ Returns a list of nodes of in-degree 0 taking into
    account lazy-removal """
    in_degree_0 = []
    for node in range(graph.size()):
        if lazy_in_degree(graph, node) == 0 and is_active(graph,node):
            in_degree_0.append(node)
    return in_degree_0

def lazy_remove_list(graph, list):
    for node in list:
        lazy_remove(graph, node)

def lazy_reset(graph):
    for node in range(graph.size()):
        lazy_add(graph, node)

def get_longest_chain(graph):
    longest_chain = deque()

    pred = np.full((graph.size()), -1, dtype=int)
    vertex_queue = deque(lazy_in_degree_0(graph))

    while len(vertex_queue) > 0:
        u = vertex_queue.popleft()
        last = u

        # iterating over the descendants of u
        # so we're cheking all edges (u->v) starting at u
        for v in graph.graph[u]:
            if v in vertex_queue:
                vertex_queue.remove(v)
            vertex_queue.append(v)
            pred[v] = u

    while last != -1:
        longest_chain.appendleft(last)
        last = pred[last]

    return longest_chain

def longest_chain_decomp(graph):
    lcd = []
    longest_chain = get_longest_chain(graph)
    while len(longest_chain) > 0:
        lcd.append(list(longest_chain))
        lazy_remove_list(graph, longest_chain)
        longest_chain = get_longest_chain(graph)
    lazy_reset(graph)

    return lcd


def test_graph(filename):
    graph = make_graph(filename)
    print(graph.graph)

    longest_chain = get_longest_chain(graph)
    print(longest_chain)

    lcd = longest_chain_decomp(graph)
    print(lcd)
    # Reproduire tous les tests qui sont dans main.cpp jusqu'a longest chain.


if __name__ == "__main__":

    test_graph("./tp2-donnees/poset10-4a")

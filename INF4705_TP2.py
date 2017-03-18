# Fichier 1 __init__.py que tu renommeras à DAG.py

# Fichier 2 INF4705_TP2.py ou whatever

from DAG import DAG # Importe la classe DAG du module DAG
import os
import sys # pour avoir accès aux arguments de ligne de commande
import numpy as np # pip install numpy

""" On avait un fichier python dans le TP1 que tu peux regarder pour savoir comment ouvrir des fichiers avec python.  Commence par hardcoder un path, laisse faire les "command line arguments" pour après que tu aies testé la création d'un graphe. """

def make_graph(filename):
	""" Returns a DAG created with a filename """

	# 0) Create a dag:
	graph = DAG.DAG()

	# 0.1) Open a file
	file = ...

	# 1) Get number of edges and number of nodes
	line = file.readline().splt()
	n_nodes = int(...)
	n_edges = int(...)
	graph.removed = np.zeros((number_of_nodes)) # Crée un numpy array
	graph.active_nodes = number_of_nodes

	# 2) Add all the nodes
	for i in range(n_nodes):
		graph.add_node(i)

	# 3) Add all the edges
	for i in range(n_edges):
		line = ... readline.split
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

def lazy_degree(graph, node):
	""" Calculates the degree of a node while taking into
	account the nodes that have been lazy-removed """
	pass

def lazy_indegree_0(graph):
	""" Returns a list of nodes of in-degree 0 taking into
	account lazy-removal """
	indegree_0 = [] #create empty list
	for node in range(graph.number_of_nodes):
		# If class DAG doesn't have a number 
		# of nodes attribute, add it in make_graph.
		if lazy_degree(graph, node) == 0 and not graph.removed[node]:
			indegree_0.append(node)




def test_graph(filename):
	graph = make_graph(filename)

	# Reproduire tous les tests qui sont dans main.cpp jusqu'a longest chain.


if __name__ == "__main__":

	test_graph("poset10-4")

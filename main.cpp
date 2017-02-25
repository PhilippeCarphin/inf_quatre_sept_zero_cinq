#include <tuple>
#include <vector>
#include <fstream>
#include <iostream>
#include <string.h>
#include <list>

typedef std::pair<int, int> Edge;
/*******************************************************************************
 * Implements a graph as an adjacency matrix and as an adjacency list
*******************************************************************************/
class Graph
{
public:
	Graph(const char *filename);
	bool is_connected(int srt, int dst);
	std::vector<int> indegree_0();
	void add_edge(Edge e);

	std::vector<std::pair<int, int> > adj_list;
	int number_of_nodes;
	int number_of_edges;
	bool *adj_mat;
	int index(int i, int j){return i*number_of_nodes + j;}
	int in_degree(int node);
};

/*******************************************************************************
 * Constructor for the graph class: The constructor takes a filename as input
 * and reads the file as a number of nodes and number of edges on the first
 * line, and the rest of the file is an adjacency list.
*******************************************************************************/
Graph::Graph(const char *filename)
{
	std::cout << __FUNCTION__ << "() called." << std::endl;
	std::ifstream f(filename , std::ios::in);

	f >> number_of_nodes;
	f >> number_of_edges;
	adj_mat = new bool[number_of_nodes*number_of_nodes];
	memset(adj_mat, 0, number_of_nodes * number_of_nodes * sizeof(bool));	
	Edge e;
	while(f >> e.first && f >> e.second){
		add_edge(e);
	}
}
/*******************************************************************************
 * Used to connect two nodes in the graph with a directed edge.
*******************************************************************************/
void Graph::add_edge(Edge e)
{
	adj_mat[index(e.first,e.second)] = 1;
	adj_list.push_back(e);
}

/*******************************************************************************
 * Returns true if there is a directed edge from src to dst and false otherwise..
*******************************************************************************/
bool Graph::is_connected(int src, int dst)
{
	return adj_mat[index(src,dst)];
}

/*******************************************************************************
 * Returns the in_degree of a node, that is, the number of edges coming into the
 * node.
*******************************************************************************/
int Graph::in_degree(int node)
{
	int in_deg = 0;
#if 1
	for(int i = 0; i < number_of_nodes; i++)
	{
		if(is_connected(i,node))
			in_deg++;
	}
#else
	for( e : adj_list ){
		// Count the number of edges that have node as their destination.
		if(e.second == node)
			in_deg++;
	}
#endif
	return in_deg;
}

/*******************************************************************************
 * Returns a list of the virtices in the graph that have in-degree 0, that is
 * the list of vertices that have no incoming edges.
 * This function looks at each nodes and adds to the list only the ones that
 * have in_degree = 0.  It uses the in_degree function.
*******************************************************************************/
std::vector<int> Graph::indegree_0()
{
	std::vector<int> v;
	for(int i = 0; i < number_of_nodes; i++)
	{

	}
	return v;
}

int main(int argc, char **argv)
{
	std::cout << "ALLO" << std::endl;
	Graph g("./tp2-donnees/poset10-4a");
	std::cout << g.number_of_nodes << std::endl;
	return 0;
}

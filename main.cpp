#include <tuple>
#include <vector>
#include <fstream>
#include <iostream>
#include <string.h>

typedef std::pair<int, int> Edge;
class Graph
{
public:
	Graph(const char *filename);
	bool is_connected(int srt, int dst);
	std::vector<int> indegree_0();
	void add_edge(Edge e);

	std::vector<std::pair<int, int>> adj_list;
	int number_of_nodes;
	int number_of_edges;
	bool *adj_mat;
	int index(int i, int j){return i*number_of_nodes + j;}
	int in_degree(int node);
};

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

std::vector<int> Graph::indegree_0()
{
	std::vector<int> v;
	for(int i = 0; i < number_of_nodes; i++)
	{

	}
	return v;
}

void Graph::add_edge(Edge e)
{
	adj_mat[index(e.first,e.second)] = 1;
	adj_list.push_back(e);
}

bool Graph::is_connected(int src, int dst)
{
	return adj_mat[index(src,dst)];
}

int Graph::in_degree(int node)
{
	int in_deg = 0;
	for(int i = 0; i < number_of_nodes; i++)
	{
		if(is_connected(i,node))
			in_deg++;
	}
	return in_deg;
}


int main(int argc, char **argv)
{
	std::cout << "ALLO" << std::endl;
	Graph g("./tp2-donnees/poset10-4a");
	std::cout << g.number_of_nodes << std::endl;
	return 0;
}
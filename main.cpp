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
	std::vector<int> get_longest_chain();

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

/*******************************************************************************
 * Longest chain algorithm
*******************************************************************************/
std::vector<int> Graph::get_longest_chain()
{
	// Input : this
	// Output :
	std::vector<int> longest_chain;
	// forall v in V pred[v] = -1
	// Tester que ceci initialise pred[v] a -1 pour chaque v
	std::vector<int> pred(number_of_nodes,-1);
	int last = -1;

	// Initialise q queue using in_degree0 function (change function to return a
	// queue while we're at it).
	std::list<int> vertex_queue; // = in_degree0();


	while(/* queue not empty find the syntax */ 1){
		// u = pop from the front and remove the element.
		// last <- u
		int u = vertex_queue.front();vertex_queue.pop_front(); // pop removes the element but does not return it. Stupid if you ask me.
		last = u;

		// forall the arcs (u,v) in E (or A for arretes)
		for( auto e : adj_list){
			// pred[v] <- u
			pred[e.second] = e.first;

			// ***** This is why we need a list and not a queue, because
			// list offers a method for removing an element from the queue,
#if 0
			if(/* find the syntax for this or write a function */ 1){
				// Move v to the end of Q
				// - remove v from the queue;
				// - put v at the end of the queue
			} else {
				// add v at the end of the queue.
			}
#endif
			// Note: Whether or not v was in the queue, we add it at the end of
			// the queue, so what we could do is
			virtex_queue.erase(v);
			virtex_queue.push_back(v);
			// because in the if and in the else, we put v at the end of the
			// queue, the only difference is that if v was in the queue, we
			// remove it to put it at the end.
		}
	} // End of while(virtex_queue not empty)

	while( last != -1){
		longest_chain.push_back(last);
		last = pred[last];
	}

	return longest_chain;
}

int main(int argc, char **argv)
{
	// Get filename from argument list
	// construct graph with that file
	std::cout << "ALLO" << std::endl;
	Graph g("./tp2-donnees/poset10-4a");
	std::cout << g.number_of_nodes << std::endl;
	return 0;
}

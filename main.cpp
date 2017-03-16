#include <tuple>
#include <cmath>
#include <vector>
#include <fstream>
#include <iostream>
#include <list>

typedef std::pair<int, int> Edge;
/*******************************************************************************
 * Removes a vertex v from list l and puts it at the back
*******************************************************************************/
int move_to_end(std::list<int> &l, const int v)
{
	for( auto itr = l.begin(); itr != l.end(); itr++)
	{
		if (*itr == v)
		{
			l.erase(itr);
			// Phil doesn't use break;
			goto end;
		}
	}
end:
	l.push_back(v);
	return 0;
}

int show_chain(std::list<int> &l)
{
	if( l.empty())
	{
		return 0;
	}

	auto node_itr = l.begin();
	std::cout << "chain : " << *node_itr;
	for(node_itr++; node_itr != l.end(); node_itr++){
		std::cout << " -> " << *node_itr;
	}
	std::cout << std::endl;

	return 1;
}

/*******************************************************************************
 * Implements a graph as an adjacency matrix and as an adjacency list
*******************************************************************************/
class Graph
{
public:
	Graph(const char *filename);
	~Graph();
	bool is_connected(int srt, int dst);
	std::list<int> indegree_0();
	void add_edge(Edge e);
	std::list<int> get_longest_chain();
	std::list< std::list<int> > longest_chain_decomp();

	int add_node(int node);
	int remove_node(int node);
	int remove_node_list(std::list<int> l);
	bool edge_removed(Edge e);
	int reset_graph();

	double entropy();
	double greedy_nle();

	bool empty();
	int backtrack();
	void __backtrack(int& count);

	std::vector<std::pair<int, int> > adj_list;
	int number_of_nodes;
	int number_of_edges;
	bool *adj_mat;
	int index(int i, int j){return i*number_of_nodes + j;}
	int in_degree(int node);

	// for doing graph algorithms
	std::vector<bool> removed;
};

/*******************************************************************************
 * Tells whether the graph is empty
*******************************************************************************/
bool Graph::empty()
{
	for( bool nr : removed ){
		if( nr == false )
			return false;
	}
	return true;
}

/*******************************************************************************
 * Backtrack routine
*******************************************************************************/
int Graph::backtrack()
{
	int count = 0;
	__backtrack(count);
	return count;
}

/*******************************************************************************
 * Backtrack internal routine
*******************************************************************************/
void Graph::__backtrack(int& count)
{
	if(empty()){
		count++;
		return;
	}

	std::list<int> indegree0 = indegree_0();
	for( int node : indegree0){
		remove_node(node);
		__backtrack(count);
		add_node(node);
	}
}
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
	removed.resize(number_of_nodes, false);
	adj_mat = new bool[number_of_nodes*number_of_nodes]();
	Edge e;
	while(f >> e.first && f >> e.second){
		add_edge(e);
	}
}

/*******************************************************************************
 * Lazy node removal
*******************************************************************************/
int Graph::remove_node(int node)
{
	removed[node] = true;
	return 0;
}

/*******************************************************************************
 * Used to add nodes back into the graph that have been lazy-removed for some
 * algorithms
*******************************************************************************/
int Graph::add_node(int node)
{
	removed[node] = false;
	return 0;
}

/*******************************************************************************
 * Used to remove the nodes of a list in the greedy algorithm
*******************************************************************************/
int Graph::remove_node_list(std::list<int> l)
{
	for( int node : l ){
		remove_node(node);
	}
	return 0;
}

int Graph::reset_graph()
{
	for(size_t i = 0; i < removed.size(); i++)
		removed[i] = false;
	return 0;
}

/*******************************************************************************
 * Destructor for the Graph class.  The only thing to do is free the memory
 * allocated for the adjacency matrix.
*******************************************************************************/
Graph::~Graph()
{
	delete [] this->adj_mat;
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
	for(int i = 0; i < number_of_nodes; i++)
	{
		if(is_connected(i,node) && (!removed[i]))
			in_deg++;
	}
	return in_deg;
}

/*******************************************************************************
 * Returns a list of the virtices in the graph that have in-degree 0, that is
 * the list of vertices that have no incoming edges.
 * This function looks at each nodes and adds to the list only the ones that
 * have in_degree = 0.  It uses the in_degree function.
*******************************************************************************/
std::list<int> Graph::indegree_0()
{
	std::list<int> v;
	for(int node = 0; node < number_of_nodes; node++)
	{
		if ( in_degree(node) == 0 && (!removed[node])){
			v.push_back(node);
		}
	}
	return v;
}

bool Graph::edge_removed(Edge e)
{
	if(removed[e.first] || removed[e.second])
		return true;
	else
		return false;
}

/*******************************************************************************
 * Longest chain algorithm
*******************************************************************************/
std::list<int> Graph::get_longest_chain()
{
	/*
	 * return value
	 */
	std::list<int> longest_chain;

	std::vector<int> pred(number_of_nodes,-1);
	std::list<int> vertex_queue = indegree_0();
	int last = -1;

	while(!vertex_queue.empty()){
		int u = vertex_queue.front();vertex_queue.pop_front();
		last = u;

		/*
		 * For all edges starting at u
		 */
		for( auto e : adj_list){
			if(!edge_removed(e)){
				if ( e.first == u ){
					int v = e.second;
					pred[v] = u;
					move_to_end(vertex_queue, v);
				}
			}
		}
	}

	while( last != -1){
		longest_chain.push_front(last);
		last = pred[last];
	}

	return longest_chain;
}

/*******************************************************************************
 * Returns a decomposition of the graph in the form of longest chains.
*******************************************************************************/
std::list< std::list<int> > Graph::longest_chain_decomp()
{
	std::list< std::list<int> > lcd;
	std::list<int> longest_chain = get_longest_chain();
	while(!longest_chain.empty()){
		lcd.push_front(longest_chain);
		remove_node_list(longest_chain);
		longest_chain = get_longest_chain();
	}
	reset_graph();
	return lcd;
}

/*******************************************************************************
 * Calculates the entropy of the graph as used to calculate the estimator for
 * the number of linear extensions.
*******************************************************************************/
double Graph::entropy()
{
	std::list< std::list<int> > lcd = longest_chain_decomp();
	double ent = 0;
	for( auto c : lcd ){
		double p = (double)c.size()/number_of_nodes;
		ent -= (p) * std::log2(p);
	}
	return ent;
}

/*******************************************************************************
 * Estimates the number of linear extensions using the formula
 * est = 2^(0.5nH)
 * where n is the number of nodes and H is the entropy of the graph.
*******************************************************************************/
double Graph::greedy_nle()
{
	double H = entropy();
	double n = number_of_nodes;
	return std::exp( 0.5 * n * H * std::log(2));
}


/*******************************************************************************
 * Display function used to show the chain decomposition.
*******************************************************************************/
void show_list_of_chains(std::list< std::list<int> > lc)
{
	for( auto c : lc){
		show_chain(c);
	}
}

int main(int argc, char **argv)
{
	//std::cout << "Working directory as seen by the program : " << system("cd") << std::endl;
	if (argc < 2){
		std::cout << "Usage " << argv[0] << " filename" << std::endl;
		return 1;
	}
	// Get filename from argument list
	const char *filename = argv[1];

	/*
	 * Testing show_chain function used to test longest chain algorithm
	 */
	std::list<int> l;
	l.push_back(1);
	l.push_back(2);
	l.push_back(3);
	l.push_back(4);
	l.push_back(5);
	show_chain(l);

	move_to_end(l, 3);
	show_chain(l);




	// construct graph with that file
	Graph g(filename);

	std::cout << "indegree_0 : ";
	l = g.indegree_0();
	show_chain(l);
	l = g.get_longest_chain();
	show_chain(l);
	std::cout << g.number_of_nodes << std::endl;
	std::cout << "Testing node removal: "<< std::endl;
	std::cout << "Indegree of node 7 (9 has an edge pointing to 7): " << g.in_degree(7) << std::endl;
	g.remove_node(9);
	std::cout << "Removing node 9 from graph" << std::endl;
	std::cout << "Indegree of node 7 (9 has an edge pointing to 7): " << g.in_degree(7) << std::endl;
	l = g.get_longest_chain();
	show_chain(l);
	g.reset_graph();
	std::cout << "Longest chain decomposition" << std::endl;
	show_list_of_chains(g.longest_chain_decomp());
	std::cout << "Entropy of g: " << g.entropy() << std::endl;
	std::cout << "Greedy number of linear extensions of g: " << g.greedy_nle() << std::endl;

	std::cout << "Backtracking algorithm result : " << g.backtrack() << std::endl;


	return 0;
}

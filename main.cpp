#include <tuple>
#include <vector>
#include <fstream>
#include <iostream>

typedef std::pair<int, int> Edge;
class Graph
{
public:
	Graph(const char *filename);

	std::vector<std::pair<int, int>> adj;
};

Graph::Graph(const char *filename)
{
	std::cout << __FUNCTION__ << "() called." << std::endl;
	std::ifstream f(filename , std::ios::in);
	Edge e;
	while(f >> e.first && f >> e.second)
		std::cout << e.first << " " << e.second << std::endl;

}
 


int main(int argc, char **argv)
{
	std::cout << "ALLO" << std::endl;
	Graph g("./tp2-donnees/poset10-4a");
	return 0;
}
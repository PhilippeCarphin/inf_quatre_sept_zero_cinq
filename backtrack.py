from lazy_DAG import lazy_DAG
import time

class Backtrack(object):
    def __init__(self):
        self.count = 0
    def __call__(self,graph):
        self.count = 0
        self.__backtrack(graph)
        return self.count
    def __backtrack(self, graph):
        if graph.empty():
            self.count += 1
            return
        for u in graph.in_degree_0():
            graph.remove_node(u)
            self.__backtrack(graph)
            graph.add_node(u)

if __name__ == "__main__":
    ld = lazy_DAG("./tp2-donnees/poset10-4a")
    print(ld.adj_dict)
    start = time.time()
    b = Backtrack()
    end = time.time()
    duration = end - start
    print("Number of linear extensions using backtrack {}".format(b(ld)))



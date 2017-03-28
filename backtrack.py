from lazy_DAG import lazy_DAG
import sys
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

def time_backtrack(filename):
    """
    Returns the time taken by the backtracking algorithm and the number of
    linear extensions
    """
    ld = lazy_DAG(filename)
    start_time = time.time()
    b = Backtrack()
    number = b(ld)
    end_time = time.time()
    duration = int( 1000000 * (end_time - start_time))
    return duration, number


if __name__ == "__main__":
    if len(sys.argv) == 1:
        ld = lazy_DAG("./tp2-donnees/poset10-4a")
        start = time.time()
        b = Backtrack()
        end = time.time()
        duration = end - start
        assert b(ld) == 1984
        print("Test passed")
    elif sys.argv >= 2:
        filename = sys.argv[1]
        duration, number = time_backtrack(filename)

        if len(sys.argv) == 2:
            print("{},{}".format(duration,number))
        elif len(sys.argv) == 3:
            print("Backtrack on file {} returned {} in {}ms".format(filename, number, duration))



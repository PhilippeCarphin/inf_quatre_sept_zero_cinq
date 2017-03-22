from collections import OrderedDict
from collections import deque
import numpy as np


class lazy_DAG(object):
    def __init__(self, filename=None, ordered_dict=None):
        if filename != None:
            file = open(filename, "r")

            first_line = file.readline().split()
            self.n_nodes = int(first_line[0])
            self.n_edges = int(first_line[1])

            # 2) Add all the nodes
            self.adj_dict = OrderedDict()
            for node in range(self.n_nodes):
                self.adj_dict[node] = set()

            # 3) Add all the edges
            for i in range(self.n_edges):
                edge = file.readline().split()
                self.adj_dict[int(edge[0])].add(int(edge[1]))

        elif ordered_dict != None:
            self.adj_dict = OrderedDict(ordered_dict)
            self.n_nodes = 0
            self.n_edges = 0
            for node in ordered_dict:
                self.n_nodes += 1
                self.n_edges += len(ordered_dict[node])
        else:
            raise exception

        self.active = np.ones((self.n_nodes)) # Cree un numpy array
        self.active_nodes = self.n_nodes

    def _is_active(self, node):
        return self.active[node]

    def empty(self):
        return self.active_nodes == 0

    def reset(self):
        self.active.fill(True)
        self.active_nodes = self.n_nodes

    def remove_node(self, node):
        if not self.active[node]:
            return
        else:
            self.active[node] = False
            self.active_nodes -= 1

    def remove_list(self, l):
        for node in l:
            self.remove_node(node)

    def add_node(self, node):
        if self.active[node]:
            return
        else:
            self.active[node] = True
            self.active_nodes += 1

    def has_edge(self, u, v):
        assert (self._is_active(u) and self._is_active(v))
        assert u < self.n_nodes and v < self.n_nodes
        return v in self.adj_dict[u]

    def nodes(self):
        return [v for v in range(self.n_nodes) if self._is_active(v)]

    def successors(self, u):
        assert self._is_active(u)
        return [v for v in self.adj_dict[u] if self._is_active(v)]

    def predecessors(self, v):
        assert self._is_active(v)
        return [u for u in self.nodes() if self.has_edge(u,v)]

    def in_degree(self, v):
        return len(self.predecessors(v))

    def in_degree_0(self):
        return [v for v in self.nodes() if self.in_degree(v) == 0]

    def adj_mat(self):
        mat = np.zeros((self.n_nodes, self.n_nodes), dtype=bool)
        for u in self.adj_dict:
            for v in self.adj_dict[u]:
                mat[u,v] = 1
        return mat
    def transitive_close_mat(self, mat):
        for k in range(self.n_nodes):
            for i in range(self.n_nodes):
                for j in range(self.n_nodes):
                    mat[i,j] = mat[i,j] or (mat[i,k] and mat[k,j])
    def adj_mat_to_adj_dict(self, mat):
        new_dict = OrderedDict()
        for u in range(self.n_nodes):
            new_dict[u] = set()
        for u in range(self.n_nodes):
            for v in range(self.n_nodes):
                if mat[u,v]:
                    new_dict[u].add(v)
        print(new_dict)
    def transitive_closure(self):
        mat = self.adj_mat()
        transitive_close_mat(mat)
        new_dict = self.adj_mat_to_adj_dict(mat)
        new_graph = lazy_DAG(new_dict)




if __name__ == "__main__":
    ld = lazy_DAG("./tp2-donnees/poset10-4a")
    ld2 = lazy_DAG(ordered_dict=ld.adj_dict)
    ld2.adj_dict[0] = "COCK"
    print(ld.adj_dict)
    print("in_degree_0():")
    print(ld.in_degree_0())
    ld.remove_node(9)
    print("in_degree_0(): after removing 9")
    print(ld.in_degree_0())
    ld.add_node(9)
    mat = ld.adj_mat()
    ld.adj_mat_to_adj_dict(mat)


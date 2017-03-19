from lazy_DAG import lazy_DAG
import numpy as np
import chains as c

def get_dimensions(lcd):
    dims = []
    for c in lcd:
        dims.append(len(c))
    return np.array(dims)

class Dynamic(object):
    def __init__(self, graph, lcd):
        self.graph = graph
        self.lcd = lcd
        # Calculate dimensions
        self.lcd_dims = get_dimensions(self.lcd)
        self.n_dims = len(self.lcd_dims)
        self.arr_dims = [d+1 for d in self.lcd_dims]
        # Create array with '-1's everywhere
        self.array = np.full(self.arr_dims, -1, dtype=int)
    def c(self,j,i_j):
        """ Returns the ith member of the jth chain """
        assert i_j < self.lcd_dims[j], "i_j = {}, dims[j] = {}".format(i_j, self.lcd_dims[j])
        return self.lcd[j][i_j]
    def delta(self, j, ps):
        """ Retuns the value delta_j for a given set of subscripts """
        for l in range(self.n_dims):
            if l == j: continue
            """ If there exists l such that (c^j_ij, c^l_il) in A """
            if self.graph.has_edge(self.c(j,ps[j]), self.c(l, ps[l])):
                return 0
        """ There doesn't exist l such that (c^j_ij, c^l_il) in A """
        return 1


if __name__ == "__main__":
    ld = lazy_DAG("./tp2-donnees/poset10-4a")

    """ Just testing the data structure """
    lcd = c.longest_chain_decomp(ld)
    print("Longest chain decomp")
    print(lcd)
    dims = get_dimensions(lcd)
    print("Dimensions : {}".format(dims))
    d1 = Dynamic(ld, lcd)
    print("Longest chain decomp dimensions : {}".format(dims))
    print("Shape of array : {}".format(d1.array.shape))
    print("==============================================================================")

    print("++++++ Testing on the graph in the enonce ++++++")
    ld = lazy_DAG("./test_graph")
    lcd = c.longest_chain_decomp(ld)
    lcd = [[1,3],[2,0]]
    d_enonce = Dynamic(ld, lcd)
    print(ld.adj_dict)
    print(lcd)
    print("Longest chain decomp dimensions : {}".format(d_enonce.lcd_dims))
    print("Shape of array : {}".format(d_enonce.array.shape))
    print("And the array itself ")
    print(d_enonce.array)

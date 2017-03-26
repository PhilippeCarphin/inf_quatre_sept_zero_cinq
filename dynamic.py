from lazy_DAG import lazy_DAG
import numpy as np
import chains as c

def get_dimensions(lcd):
    dims = []
    for c in lcd:
        dims.append(len(c))
    return np.array(dims)

def decr(j, ps):
    return ps[:j] + (ps[j] - 1,) + ps[j+1:]

class Dynamic(object):
    def __init__(self, graph, lcd, copy=True):
        """ Creates an array to be filled by the dynamic programming algotithm.

        PARAMETERS
        ==========
            graph:  Reference to the graph.
            lcd: A decomposition of the graph into chains.

        ATTRIBUTES
        ==========

            n_dims : The number of dimensions of the array
            lcd_dims : the length of the chains.  This corresponds to the m_k's
                       in the enonce
            arr_dims : This is a list of m_k + 1.  Indeed, we can look at the
                       example and notice that the array is 3x3 whereas the
                       chains are of length 2.
            array : a numpy array that will be filled by the dynamic programming
                    algorithm.

        NOTES
        =====

            By default, the graph is copied so as not to modify the graph that
            was passed since it is a reference, but by specifying copy=False, we
            can save the time of copying the graph.
        """
        if copy == True:
            self.graph = graph.transitive_closure()
        else:
            self.graph = graph
            self.graph.transitive_close()

        self.lcd = lcd

        # Calculate dimensions
        self.n_dims = len(lcd)
        self.lcd_dims = tuple([len(c) for c in lcd])
        self.arr_dims = tuple([d+1 for d in self.lcd_dims])

        # Create array with '-1's everywhere so we are able to tell whether or
        # not a value has already been calculated.
        self.array = np.full(self.arr_dims, -1, dtype=int)
        self.array[tuple([0 for i in self.arr_dims])] = 1

    def c(self,j,i_j):
        """ Returns the ith member of the jth chain """
        """ The index j of the chains goes from 0 to k-1 (where k is the 
        number of chains in our decomposition """
        assert j < len(lcd), "j must be the index of a chain"
        """ The index i_j goes from 0 to len(lcd[j]) this range is one longer
        than the length of the chain because we go from {} to the full chain. """
        assert i_j <= self.lcd_dims[j], "i_j = {}, dims[j] = {}".format(i_j, self.lcd_dims[j])
        if i_j == 0:
            return None
        else:
            return self.lcd[j][i_j-1]

    def delta(self, j, ps):
        if j < 0: return 0
        """ Retuns the value delta_j for a given set of subscripts """
        for l in range(self.n_dims):
            """ Don't check when k == j, it makes no sense """
            if l == j: continue
            """ If there exists l such that (c^j_ij, c^l_il) in A """
            if self.graph.has_edge(self.c(j,ps[j]), self.c(l, ps[l])):
                return 0
        """ There doesn't exist l such that (c^j_ij, c^l_il) in A """
        return 1

    def __str__(self):
        return """ graph : {}
    lcd : {}
    n_dims : {}
    lcd_dims : {}
    array_dims : {}
    array :
{} """.format(self.graph.adj_dict, self.lcd, self.n_dims, self.lcd_dims,
    self.arr_dims, self.array)

    def set_index(self, ps):
        """ if ps has the form (0,...,0,n,0,...,0), that is it has only one
        non-zero element, then we are asking for the number of linear extensions
        for a chain of lenght n.  There is only one linear extension. """
        # num_non_zero = 0
        # for i in ps:
        #     if i != 0:
        #         num_non_zero += 1

        # if num_non_zero <= 1:
        #     self.array[ps] = 1
        # else:
        """ value = the sum of other elements in the array as described in that
        formula. """
        value = self.sum_of_adjacents(ps)
        print("set_index({}) setting to {}".format(ps, value))
        self.array[ps] = value


    def sum_of_adjacents(self, ps):
        value = 0
        flag = False
        for j in [i for i in range(self.n_dims) if ps[i] > 0]:

            if self.delta(j,ps) == 0: continue
            new_ps = decr(j, ps) # copy

            if self.array[new_ps] == -1:
                self.set_index(new_ps)

            # print("  array({}) = {}".format(ps, self.array[tuple(ps)]))
            value += self.array[new_ps]
            flat = True
        # print(" ... Setting array({}) to {}".format(ps, value))
        return value

    def fill(self):
        self.set_index(self.lcd_dims)
        return self.array[tuple(self.lcd_dims)]

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
    lcd = c.longest_chain_decomp(ld)
    lcd = [[1,3],[2,0]]
    d_enonce = Dynamic(ld, lcd)
    print(ld.adj_dict)
    print(lcd)
    tup = (0,1)
    d_enonce.set_index(tup)
    d_enonce.fill()
    print(d_enonce)
    print(d_enonce.fill())
    ld = lazy_DAG("./tp2-donnees/poset10-4a")
    lcd = c.longest_chain_decomp(ld)
    d1 = Dynamic(ld, lcd)
    print(d1.fill())

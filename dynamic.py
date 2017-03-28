import sys
from lazy_DAG import lazy_DAG
import numpy as np
import chains as c
import time

def decr(j, ps):
    """ For a tuple of the form (a,b,c,d,e,f) returns a copy of that tuple 
    where the element at index j has been decremented by one. """
    return ps[:j] + (ps[j] - 1,) + ps[j+1:]

class Dynamic(object):
    def __init__(self, graph, lcd, copy=True):
        """ This object encapsulates an array to be used for the dynamic 
        programming algorithm.  It also keeps track of certain elements 
        necessary for the execution of the algorithm that will be described 
        in the ATTRIBUTES section.

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
        self.arr_dims = tuple([mk+1 for mk in self.lcd_dims])

        # Create array with '-1's everywhere so we are able to tell whether or
        # not a value has already been calculated.
        self.array = np.full(self.arr_dims, -1, dtype=int)
        self.array[tuple([0 for i in self.arr_dims])] = 1

    def c(self,j,i_j):
        """ Returns the ith member of the jth chain """
        """ The index j of the chains goes from 0 to k-1 (where k is the 
        number of chains in our decomposition """
        assert j < len(self.lcd), "j must be the index of a chain"
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
        self.array[ps] = self.sum_of_adjacents(ps)

    def sum_of_adjacents(self, ps):
        value = 0
        for j in [i for i in range(self.n_dims) if ps[i] > 0]:
            if self.delta(j,ps) == 0:
                continue
            new_ps = decr(j, ps) # copy
            if self.array[new_ps] == -1:
                self.set_index(new_ps)
            value += self.array[new_ps]
        return value

    def fill(self):
        self.set_index(self.lcd_dims)
        return self.array[tuple(self.lcd_dims)]

def time_dynamic(filename):
    ld = lazy_DAG(filename)
    start_time = time.time()
    lcd = c.longest_chain_decomp(ld)
    d = Dynamic(ld, lcd)
    number = d.fill()
    end_time = time.time()
    duration = int( 1000000 * (end_time - start_time))
    return duration, number

if __name__ == "__main__":
    if len(sys.argv) == 1:
        assert time_dynamic("./tp2-donnees/poset10-4a")[1] == 1984
        assert time_dynamic("./tp2-donnees/poset10-8a")[1] == 332640
        assert time_dynamic("./tp2-donnees/poset14-8e")[1] == 52972920
        print("\n{} : Tests passed".format(sys.argv[0]))
    elif sys.argv >= 2:
        filename = sys.argv[1]
        duration, number = time_dynamic(filename)

        if len(sys.argv) == 2:
            print("{},{}".format(duration,number))
        elif len(sys.argv) == 3:
            print("Dynamic on file {} returned {} in {}us".format(filename, number, duration))



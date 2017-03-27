from lazy_DAG import lazy_DAG
from chains import Chain
import chains as ch
import math as m
import time
import sys

def entropy(graph, lcd):
    ent = 0
    for c in lcd:
        p = float(len(c))/graph.n_nodes
        ent -= p * m.log(p,2)
    return ent

def greedy_estimator(graph, lcd):
    H = entropy(graph, lcd)
    n = graph.n_nodes
    return 2 ** (0.5 * n * H)

def time_entropy(filename):
    ld = lazy_DAG(filename)
    start_time = time.time()
    lcd = ch.longest_chain_decomp(ld)
    number = greedy_estimator(ld,lcd)
    end_time = time.time()
    duration = int( 1000000 * (end_time - start_time))
    return duration, number

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ld = lazy_DAG("./tp2-donnees/poset10-4a")
        lcd = ch.longest_chain_decomp(ld)
        print(lcd)
        print(entropy(ld, lcd))
        print(m.log(8,2))
        print(greedy_estimator(ld, lcd))
    elif sys.argv >= 2:
        filename = sys.argv[1]
        duration, number = time_entropy(filename)

        if len(sys.argv) == 2:
            print(duration)
        elif len(sys.argv) == 3:
            print("Entropy on file {} returned {} in {}us".format(filename, number, duration))



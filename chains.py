import lazy_DAG
from collections import deque
from lazy_DAG import lazy_DAG

class Chain(deque):
    def __init__(self, pred_dict, last):
        assert type(last) is int ,"type last is {}".format(type(last))
        chain = deque()
        while last in pred_dict:
            self.appendleft(last)
            last = pred_dict[last]
        self.appendleft(last)

def move_to_end(q,v):
    try: q.remove(v)
    except: pass
    q.append(v)

def longest_chain(graph):
    if graph.empty():
        return None
    vertex_queue = deque(graph.in_degree_0())
    assert len(vertex_queue) > 0 , "non-empty graph cannot have empty in_degree_0"
    pred_dict = {}
    while len(vertex_queue) > 0:
        u = vertex_queue.popleft()
        last = u
        for v in graph.successors(u):
            move_to_end(vertex_queue,v)
            pred_dict[v] = u
    return Chain(pred_dict, last)

def longest_chain_decomp(graph):
    lcd = []
    while True:
        lc = longest_chain(graph)
        if lc == None: break
        lcd.append(list(lc))
        graph.remove_list(lc)
    graph.reset()
    return lcd

if __name__ == "__main__":

    ld = lazy_DAG("./tp2-donnees/poset10-4a")
    print(ld.adj_dict)
    print("Longest chain:")
    print(longest_chain(ld))

    lcd = longest_chain_decomp(ld)
    print("Longest chain: decomposition")
    print(lcd)

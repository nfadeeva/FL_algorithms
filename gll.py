from collections import defaultdict
from utils import *
from itertools import chain
import sys
import time


class GSS:
    def __init__(self):
        self.v=defaultdict(lambda: defaultdict(set))


def gll(R, g):
    working_list = set()
    history = set()
    poped = defaultdict(list)
    gss = GSS()
    res = set()

    # create starts configurations from every node in graph in every nonterminal in grammar
    for i in range(len(R)):
        for j in g.starts:
            for k in g.starts[j]:
                working_list.add((i,k,(j,i)))
    start = time.time()
    while working_list:
        end = time.time()
        if (end - start) // 60:
            start = time.time()
            print("test is working, len of result for now = "
                  "{length}".format(length=len(res)))

        i_graph, i_grammar, gss_node = working_list.pop()
        if (i_graph, i_grammar, gss_node) in history:
            continue
        history.add((i_graph, i_grammar, gss_node))

        # 3 case
        if i_grammar in chain(*g.fins.values()):
            # pop
            working_list.update((i_graph, x, j) for j in gss.v[gss_node] for x in gss.v[gss_node][j])
            res.add((gss_node[1], gss_node[0], i_graph))
            poped[gss_node].append(i_graph)
        for j_grammar, labels_grammar in enumerate(g.G[i_grammar]):
            for j_graph, labels_graph in enumerate(R[i_graph]):

                for label_grammar in labels_grammar:
                    # 2 case
                    if label_grammar not in g.terminals:
                        gss.v[(label_grammar, i_graph)][gss_node].add(j_grammar)
                        gss_node_new = (label_grammar, i_graph)
                        for st in g.starts[label_grammar]:
                            working_list.add((i_graph, st, gss_node_new))

                        # pop again
                        if gss_node_new in poped:
                            # pop
                            for v in poped[gss_node_new]:
                                if (v, j_grammar, gss_node) not in history:
                                    working_list.add((v, j_grammar, gss_node))
                    # 1 case
                    for label_graph in labels_graph:
                        if label_grammar == label_graph and label_grammar in g.terminals:
                            working_list.add((j_graph, j_grammar, gss_node))

    return res

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("len of arguments < 3, please, start the script like this:"
              "python3 gll.py data/my_test_grammar_automata data/my_test_graph [result.txt]")
        sys.exit()

    G = parse_grammar_automata(sys.argv[1])
    R = parse_graph(sys.argv[2])
    result = gll(R, G)
    if len(sys.argv) == 3:
        print('\n'.join(map(str, result)))
    else:
        with open(sys.argv[3],'w') as f:
            f.write('\n'.join(map(str, result)))

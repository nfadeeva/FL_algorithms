import re
from collections import defaultdict
from utils import parse_graph
from itertools import chain
import sys
import time


class GSS:
    def __init__(self):
        self.v=defaultdict(lambda: defaultdict(set))


class GrammarAutomata:
    def __init__(self):
        self.starts = defaultdict(list)
        self.fins = defaultdict(list)
        self.terminals = set()
        self.G = None


def parse_grammar_automata(filename):
    g = GrammarAutomata()
    with open(filename,'r') as f:
        lines = f.readlines()
    size = lines[2].count(";")
    g.G = [[[] for i in range(size)] for i in range(size)]

    # fill starts
    for line in lines[3:]:
        line_ = re.findall('(\d+)\[label="(\w+)", \w*color="green"\]', line)
        if line_:
            state, nonterminal = line_[0]
            g.starts[nonterminal].append(int(state))

    # fill fins
    for line in lines[3:]:
        line_ = re.findall('(\d+)\[label="(\w+)", shape="doublecircle"*', line)
        if line_:
            state, nonterminal = line_[0]
            g.fins[nonterminal].append(int(state))

    for line in lines[3:]:
        line_ = re.findall('(\d+) -> (\d+)\[label = "(\w+|.)"\]', line)
        if line_:
            i, j, label = line_[0]
            g.G[int(i)][int(j)].append(label)
            if not label.isupper():
                g.terminals.add(label)
    return g


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
                        gss_node1 = (label_grammar, i_graph)
                        for st in g.starts[label_grammar]:
                            working_list.add((i_graph, st, gss_node1))

                        # pop again
                        if gss_node1 in poped:
                            # pop
                            for v in poped[gss_node1]:
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

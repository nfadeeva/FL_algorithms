# python3 trans_closure.py data/grammars/my_test_grammar data/graphs/my_test_graph [result.txt]
import re
from collections import defaultdict
from utils import parse_graph
import sys
import time


class Grammar:
    def __init__(self):
        # terminals
        self.T = set()
        # inverted rules of grammar (S->AB ~ R[(A,B)]=[S])
        self.R = defaultdict(list)


def trans_closure(R, G):
    flag = True
    size = len(R)
    m = [[[] for i in range(size)] for i in range(size)]

    # replace terminals with nonterminals
    for i in range(size):
        for j in range(size):
            for element in R[i][j]:
                if element in G.T:
                    m[i][j].extend(G.R[(element,)])

    start = time.time()
    while flag:
        flag = False
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    for i_ in m[i][k]:
                        for j_ in m[k][j]:
                            for z in G.R.get((i_, j_),[]):
                                    end = time.time()
                                    if (end - start) // 60:
                                        start = time.time()
                                        cur_res = [(i, label, j)
                                         for i in range(size) for j in range(size)
                                         for label in m[i][j]]
                                        print("test is working, len of result for now = "
                                              "{length}".format(length=len(cur_res)))
                                    if z not in m[i][j]:
                                        m[i][j].append(z)
                                        flag = True


    return [(i, label, j)
            for i in range(size) for j in range(size)
            for label in m[i][j]]


def parse_grammar_hom(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    gr = Grammar()
    for line in lines:
        rule = re.findall(r'(\w+) -> (\w+) (\w+)', line)
        if rule:
            left, right_1, right_2 = rule[0]
            gr.R[(right_1, right_2)].append(left)

        # rule looks like S -> a
        else:
            rule = re.findall(r'(\w+) -> (\w+)', line)
            left, terminal = rule[0]
            gr.T.add(terminal)
            gr.R[(terminal,)].append(left)
    return gr


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("len of arguments < 3, please, start the script like this:"
              "# python3 trans_closure.py data/my_test_grammar data/my_test_graph [result.txt]")
        sys.exit()

    G1 = parse_grammar_hom(sys.argv[1])
    graph = parse_graph(sys.argv[2])
    result = trans_closure(graph, G1)
    print(G1.R, G1.T)
    if len(sys.argv) == 3:
        pass
        #print('\n'.join(map(str,result)))
    else:
        with open(sys.argv[3],'w') as f:
            f.write('\n'.join(map(str,result)))

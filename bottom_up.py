# python3 bottom_up.py data/grammars/my_test_grammar data/graphs/my_test_graph [result.txt]
from utils import parse_graph
from collections import defaultdict
import time
import sys


class Grammar:
    def __init__(self):
        self.G = None
        self.eps_nonterminals = None


def parse_grammar(filename):
    gr = Grammar()
    gr.G = defaultdict(list)
    gr.eps_nonterminals = set()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            l, r = line.split(' -> ')
            r = r.rstrip('\n')
            gr.G[l].append(r.split(' '))
            if r == "eps":
                gr.eps_nonterminals.add(l)
    return gr


def bottom_up(R, gr):

    G = gr.G
    eps_nonterminals = gr.eps_nonterminals
    def traverse(R, start, end, string, G):
        for r in G:
            # if string is nonterminal
            if string in G[r]:
                if r not in R[start][end]:
                    R[start][end].append(r)
                    nonlocal flag
                    flag = True
        nonlocal max_len
        if len(string) == max_len:
            return
        for k in range(len(R[end])):
            if not R[end][k]:
                continue
            for label in R[end][k][:]:
                traverse(R, start, k, string + [label], G)
        return

    size = len(R)
    # add loop for every node with label = A if there is A->eps
    for i in range(size):
        R[i][i].extend(eps_nonterminals)
    flag = True
    start = time.time()
    while flag:
        flag = False
        max_len = max(len(x) for k in G.values() for x in k)
        for i in range(size):
            traverse(R, i, i, [], G)
        end = time.time()
        if (end - start) // 60:
            start = time.time()
            cur_res = [(i, label, j)
            for i in range(size) for j in range(size)
            for label in R[i][j] if label in G.keys()]
            print("test is working, len of result for now = "
                  "{length}".format(length=len(cur_res)))
    return [(i, label, j)
            for i in range(size) for j in range(size)
            for label in R[i][j] if label in G.keys()]

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("len of arguments < 3, please, start the script like this:"
              "python3 bottom_up.py data/my_test_grammar data/my_test_graph [result.txt]")
        sys.exit()

    G = parse_grammar(sys.argv[1])
    R = parse_graph(sys.argv[2])
    result = bottom_up(R, G)

    if len(sys.argv) == 3:
        print('\n'.join(map(str,result)))
    else:
        with open(sys.argv[3],'w') as f:
            f.write('\n'.join(map(str,result)))

from utils import parse_graph
from collections import defaultdict
import sys
# python3 bottom_up.py data/grammars/my_test_grammar data/graphs/my_test_graph [result.txt]


def parse_grammar(filename):
    G = defaultdict(list)
    eps_nonterminals = set()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            l, r = line.split(' -> ')
            r = r.rstrip('\n')
            G[l].append(r.split(' '))
            if r == "eps":
                eps_nonterminals.add(l)
    return G, eps_nonterminals


def bottom_up(R, G, eps_nonterminals):

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
    while flag:
        flag = False
        max_len = max(len(x) for k in G.values() for x in k)
        for i in range(size):
            traverse(R, i, i, [], G)
    return [(i, label, j)
            for i in range(size) for j in range(size)
            for label in R[i][j] if label in G.keys()]

if __name__ == 'main':

    if len(sys.argv) < 3:
        print("len of arguments < 3, please, start the script like this:"
              "python3 bottom_up.py data/my_test_grammar data/my_test_graph [result.txt]")
        sys.exit()

    G, eps_nonterminals = parse_grammar(sys.argv[1])
    R = parse_graph(sys.argv[2])
    result = bottom_up(R, G, eps_nonterminals)

    if len(sys.argv) == 3:
        print('\n'.join(map(str,result)))
    else:
        with open(sys.argv[3],'w') as f:
            f.write('\n'.join(map(str,result)))

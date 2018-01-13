# python3 bottom_up.py data/grammars/grammar_automata_0 data/graphs/graph_0 [result.txt]
from utils import *
import time
import sys


def bottom_up(R, gr):

    def traverse(R, G, nonterm, history):

        start_graph, start_grammar = history[0]
        end_graph, end_grammar = history[-1]

        if end_grammar in gr.fins[nonterm]:
            if nonterm not in R[start_graph][end_graph]:
                R[start_graph][end_graph].append(nonterm)
                nonlocal flag
                flag = True

        for new_end_graph in range(len(R[end_graph])):
            if not R[end_graph][new_end_graph]:
                continue
            labels_graph = R[end_graph][new_end_graph]
            for new_end_grammar, labels_grammar in enumerate(G[start_grammar]):
                for label_grammar in G[end_grammar][new_end_grammar]:
                    if label_grammar in labels_graph:
                        if (new_end_graph, new_end_grammar) not in history:
                            new_history = history[:]
                            new_history.append((new_end_graph, new_end_grammar))
                            traverse(R, G, nonterm, new_history)

        return
    G = gr.G
    size = len(R)
    flag = True
    start = time.time()
    while flag:
        flag = False
        for start_nonterm in gr.starts:
            for i in range(size):
                for start_grammar in gr.starts[start_nonterm]:
                    traverse(R, G, start_nonterm, [(i, start_grammar)])

        end = time.time()
        if (end - start) // 60:
            start = time.time()
            cur_res = [(i, label, j)
            for i in range(size) for j in range(size)
            for label in R[i][j] if label in gr.starts]
            print("test is working, len of result for now = "
                  "{length}".format(length=len(cur_res)))

    return [(i, label, j)
            for i in range(size) for j in range(size)
            for label in R[i][j] if label in gr.starts]

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("len of arguments < 3, please, start the script like this:"
              "python3 bottom_up.py data/my_test_grammar_automata data/my_test_graph [result.txt]")
        sys.exit()

    G = parse_grammar_automata(sys.argv[1])
    R = parse_graph(sys.argv[2])
    result = bottom_up(R, G)

    if len(sys.argv) == 3:
        print('\n'.join(map(str,result)))
    else:
        with open(sys.argv[3],'w') as f:
            f.write('\n'.join(map(str,result)))
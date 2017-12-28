import re
from collections import defaultdict

# for gll
class GrammarAutomata:
    def __init__(self):
        self.starts = defaultdict(list)
        self.fins = defaultdict(list)
        self.terminals = set()
        self.G = None

# for glr
class Grammar:
    def __init__(self):
        self.G = defaultdict(list)
        self.eps_nonterminals = set()

# for trans_closure
class GrammarHom:
    def __init__(self):
        # terminals
        self.T = set()
        # inverted rules of grammar (S->AB ~ R[(A,B)]=[S])
        self.R = defaultdict(list)

def parse_grammar_hom(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    gr = GrammarHom()
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


def dfs(graph_matrix,start,goal):
    def matrix_to_list(matrix):
        graph = {}
        for i, node in enumerate(matrix):
            adj = set()
            for j, connected in enumerate(node):
                if connected:
                    adj.add(j)
            graph[i] = adj
        return graph

    def dfs_paths(graph, start, goal, path=None):
        if start == goal:
             yield path + [x for x in graph_matrix[start][goal]]
        if not path:
            path=[]
        for next in graph[start] - set(path):
            for x in graph_matrix[start][next]:
                yield from dfs_paths(graph, next, goal, path + [x])
    return dfs_paths(matrix_to_list(graph_matrix), start, goal)

def graph_to_grammar(G):
    gr = Grammar()
    for start_nonterminal in G.starts:
        for start_state in G.starts[start_nonterminal]:
            for fin_state in G.fins[start_nonterminal]:
                gr.G[start_nonterminal].extend(dfs(G.G, start_state, fin_state))
                if ['eps'] in gr.G[start_nonterminal]:
                    gr.eps_nonterminals.add(start_nonterminal)
    return gr

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



def parse_graph(filename):
    """:returns adjacency matrix R"""

    with open(filename) as f:
        lines = f.readlines()
        size = lines[2].count(";")
        R = [[[] for i in range(size)] for i in range(size)]
        for line in lines[2:]:
            line_ = re.findall('(\d+) -> (\d+)\[label="(\w+|.)"\]', line)
            if line_:
                i, j, label = line_[0]
                R[int(i)][int(j)].append(label)
    return R

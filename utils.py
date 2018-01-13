import re
from collections import defaultdict

# for gll
class GrammarAutomata:
    def __init__(self):
        self.starts = defaultdict(list)
        self.fins = defaultdict(list)
        self.terminals = set()
        self.G = None


# for trans_closure
class GrammarHom:
    def __init__(self):
        # terminals
        self.T = set()
        # inverted rules of grammar (S->AB ~ R[(A,B)]=[S])
        self.R = defaultdict(list)
        # set of eps_nonterminals (A -> eps)
        self.eps_nonterminals = set()



def parse_grammar_hom(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    gr = GrammarHom()
    for line in lines:
        line = line.replace(" -> ",'->')
        line = line.replace(" = ",'=')
        rule = re.findall(r'(\w+)->(\w+) (\w+)', line)
        if rule:
            left, right_1, right_2 = rule[0]
            gr.R[(right_1, right_2)].append(left)

        # rule looks like S -> a
        else:
            rule = re.findall(r'(\w+)->(\w+)', line)
            left, terminal = rule[0]
            gr.T.add(terminal)
            gr.R[(terminal,)].append(left)
            if terminal == "eps":
                gr.eps_nonterminals.add(left)

    return gr


def parse_grammar_automata(filename):
    g = GrammarAutomata()
    with open(filename,'r') as f:
        lines = f.readlines()
    size = lines[2].count(";")
    g.G = [[[] for i in range(size)] for i in range(size)]
    # fill starts
    for line in lines[3:]:
        line = line.replace(" = ", '=')
        line_ = re.findall('(\d+)\[label="(\w+)",[\w|=, "]*color="green"\]', line)
        if line_:
            state, nonterminal = line_[0]
            g.starts[nonterminal].append(int(state))
    # fill fins
    for line in lines[3:]:
        line = line.replace(" = ", '=')
        line_ = re.findall('(\d+)\[label="(\w+)", shape="doublecircle"*', line)
        if line_:
            state, nonterminal = line_[0]
            g.fins[nonterminal].append(int(state))


    for line in lines[3:]:
        line = line.replace(" -> ",'->')
        line = line.replace(" = ",'=')
        line_ = re.findall('(\d+)->(\d+)\[label="(\w+|.)"\]', line)
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
            line = line.replace(" -> ", '->')
            line = line.replace(" = ", '=')
            line_ = re.findall('(\d+)->(\d+)\[label="(\w+|.)"\]', line)
            if line_:
                i, j, label = line_[0]
                R[int(i)][int(j)].append(label)
    return R

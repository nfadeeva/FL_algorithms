import re


def parse_graph(filename):
    """:returns adjacency matrix R"""

    with open(filename) as f:
        lines = f.readlines()
        size = lines[2].count(";")
        R = [[[] for i in range(size)] for i in range(size)]
        for line in lines[2:]:
            line_ = re.findall('(\d+) -> (\d+)\[label="(\w+)"\]', line)
            if line_:
                i, j, label = line_[0]
                R[int(i)][int(j)].append(label)
    return R

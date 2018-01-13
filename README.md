# FL_algorithms
- trans_closure.py
- bottom_up.py
- gll.py
## Requirements:
python3 and pytest

### How to install pytest:
``` 
pip3 install pytest
``` 
## Input data:
- trans_closure.py - grammar in Chomsky normal form (grammars/*_hom)
- bottom_up.py - grammars in graph representation (grammars/*_automata)
- gll.py - grammars in graph representation (grammars/*_automata)
## How to run every algorithm:
``` 
python3 bottom_up.py data/grammars/grammar_automata_0 data/graphs/graph_0 [result.txt]
```

```
python3 trans_closure.py data/grammars/grammar_hom_0 data/graphs/graph_0 [result.txt]
```

```
python3 gll.py data/grammars/grammar_automata_0 data/graphs/graph_0 [result.txt]
```
## Unittests
### There are five tests: 
- test_0 (grammar_automata_0, graph_0) -  general test for many difficult cases(cycles in graph and grammar, many labels on one transition)
- test_1 (grammar_automata_1, graph_1) - grammar with cycle + very simple graph(linear)
- test_2 (grammar_automata_1, graph_1_1) - grammar with cycle + graph with cycle
- test_3 (grammar_automata_2, graph_1) - grammar_automata_1 with S->eps + simple graph
- The last test compares results of algorithms for all graphs and grammars in the document
#### Run all tests:
```
pytest test.py -s
```
-s for print messages while testing
#### Run specific test:
```
pytest test.py::test_my_example_0 -s
```
```
pytest test.py::test_my_example_1 -s
```
```
pytest test.py::test_my_example_2 -s
```
```
pytest test.py::test_my_example_3 -s
```
```
pytest test.py::test_doc_graphs -s
```
Test_doc_graphs runs on all graphs, grammars and algorithms

You can change settings of test_doc_graphs in test.py to specify which grammar, algorithm would you like to test and set up the number of graphs from the document
```
BOTTOM_UP = True
TRANS_CLOSURE = True
GLL = True
NUM = 11 # it means that test will be run from 0 to 11 graph
Q1_ = True
Q2_ = True
```

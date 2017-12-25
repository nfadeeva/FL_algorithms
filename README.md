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
- bottom_up.py - grammars
- gll.py - grammars in graph representation (grammars/*_automata)
## How to run every algorithm:
``` 
python3 bottom_up.py data/grammars/my_test_grammar data/graphs/my_test_graph result.txt
```

```
python3 trans_closure.py data/grammars/my_test_grammar data/graphs/my_test_graph result.txt
```

```
python3 gll.py data/grammars/my_test_grammar_automata data/graphs/my_test_graph result.txt
```
## Unittest
### There are two tests: 
- First test is my example for data/grammars/my_test_grammar and data/graphs/my_test_graph
- The second test compares results of algorithms for all graphs and grammars in the document
#### Run all test:
```
pytest test.py -s
```
-s for print messages while testing
#### Run specific test:
```
pytest test.py::test_my_example -s
```
```
pytest test.py::test_doc_graphs -s
```
You can change settings of test_doc_graphs in test.py to specify which grammar, algorithm would you like to test and set up the number of graphs from the document
```
BOTTOM_UP = True
TRANS_CLOSURE = True
GLL = True
NUM = 11 # number of graphs to test (0..11)
Q1_ = True
Q2_ = True
```

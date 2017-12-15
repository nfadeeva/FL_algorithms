# FL_algorithms
- trans_closure.py
- bottom_up.py
## Requirements:
python3

## How to run every algorithm:
``` 
python3 bottom_up.py data/grammars/my_test_grammar data/graphs/my_test_graph result.txt
```

```
python3 trans_closure.py data/grammars/my_test_grammar data/graphs/my_test_graph result.txt
```
## Unittest
### There are two tests: 
- First test is my example for data/grammars/my_test_grammar and data/graphs/my_test_graph
- The second test compares results of algorithms for all graphs and grammars in the document
#### Run test:
```
python3 -m unittest test.py
```

from trans_closure import *
from bottom_up import *
from gll import *
from utils import parse_graph
import os


BOTTOM_UP = False
TRANS_CLOSURE = False
GLL = True
NUM = -6


def test_my_example():
    right_result = {(0, 'S1', 0), (0, 'S5', 0),
                    (0, 'S', 0), (0, 'S3', 1),
                    (0, 'S', 2), (0, 'S6', 2),
                    (1, 'S5', 0), (1, 'S3', 2),
                    (1, 'S', 2), (1, 'S6', 2),
                    (2, 'S2', 0), (2, 'S4', 2)}

    G = parse_grammar("data/grammars/my_test_grammar")
    G_hom = parse_grammar_hom("data/grammars/my_test_grammar")
    G_automata = parse_grammar_automata("data/grammars/my_test_grammar_automata")
    if TRANS_CLOSURE:
        result_closure = trans_closure(parse_graph("data/graphs/my_test_graph"), G_hom)
        assert set(result_closure) == right_result
        print("test for my_graph and my_grammar - trans_closure - OK")

    if BOTTOM_UP:
        result_bottom_up = bottom_up(parse_graph("data/graphs/my_test_graph"), G)
        assert set(result_bottom_up) ==right_result
        print("test for my_graph and my_grammar - bottom_up - OK")

    if GLL:
        result_gll = gll(parse_graph("data/graphs/my_test_graph"), G_automata)
        assert set(result_gll) ==right_result
        print("test for my_graph and my_grammar - gll - OK")


def test_doc_graphs():
    with open('data/data_for_tests/graphs') as f:
        graphs = ['data/graphs/data/'+ x for x in f.read().splitlines()]

    # q1
    with open('data/data_for_tests/q1_answers') as f:
        right_q1 = [int(x) for x in f.read().splitlines()]

    Q1_hom = parse_grammar_hom('data/grammars/Q1_hom')
    Q1= parse_grammar('data/grammars/Q1')
    Q1_automata= parse_grammar_automata('data/grammars/Q1_automata')

    graphs = graphs[:NUM]
    right_q1= right_q1[:NUM]

    for graph, answer in zip(graphs, right_q1):
        print("start test for {graph} and {grammar}".format(
            graph=os.path.basename(graph), grammar='Q1'))
        if TRANS_CLOSURE:
            res = trans_closure(parse_graph(graph), Q1_hom)
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar}- trans_closure OK".format(
                graph=os.path.basename(graph), grammar='Q1'))

        if BOTTOM_UP:
            res = bottom_up(parse_graph(graph), Q1)
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar}- bottom_up OK".format(
                graph=os.path.basename(graph), grammar='Q1'))

        if GLL:
            res = gll(parse_graph(graph), Q1_automata)
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar} - gll OK".format(
                graph=os.path.basename(graph), grammar='Q1'))
            print()

    # q2
    with open('data/data_for_tests/q2_answers') as f:
        right_q2 = [int(x) for x in f.read().splitlines()]
    Q2 = parse_grammar('data/grammars/Q2')
    Q2_hom = parse_grammar_hom('data/grammars/Q2_hom')
    Q2_automata = parse_grammar_automata('data/grammars/Q2_automata')


    graphs = graphs[:NUM]
    right_q2= right_q2[:NUM]
    for graph, answer in zip(graphs, right_q2):

        if TRANS_CLOSURE:
            res = trans_closure(parse_graph(graph), Q2_hom)
            print("start test for {graph} and {grammar}".format(
                graph=os.path.basename(graph), grammar='Q2'))
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar}- trans_closure OK".format(
                graph=os.path.basename(graph), grammar='Q2'))

        if BOTTOM_UP:
            res = bottom_up(parse_graph(graph), Q2)
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar}- bottom_up OK".format(
                graph=os.path.basename(graph), grammar='Q2'))

        if GLL:
            res = gll(parse_graph(graph), Q2_automata)
            assert (len(list(filter(lambda x: x[1] == 'S', res)))) == answer
            print("test for {graph} and {grammar} - gll OK".format(
                graph=os.path.basename(graph), grammar='Q2'))
            print()

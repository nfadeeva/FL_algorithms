import unittest
from trans_closure import *
from bottom_up import *
from utils import parse_graph

class Tests(unittest.TestCase):

    def test_my_example(self):
        R = parse_graph("data/graphs/my_test_graph")
        right_result = {(0, 'S1', 0), (0, 'S5', 0),
                        (0, 'S', 0), (0, 'S3', 1),
                        (0, 'S', 2), (0, 'S6', 2),
                        (1, 'S5', 0), (1, 'S3', 2),
                        (1, 'S', 2), (1, 'S6', 2),
                        (2, 'S2', 0), (2, 'S4', 2)}

        G, eps_nonterminals = parse_grammar("data/grammars/my_test_grammar")
        result_bottom_up = bottom_up(R, G, eps_nonterminals)
        self.assertEqual(set(result_bottom_up), right_result)

        G_hom = parse_grammar_hom("data/grammars/my_test_grammar")
        result_closure = trans_closure(R, G_hom)
        self.assertEqual(set(result_closure), right_result)

    def test_all_graphs_and_grammars(self):
        graphs = list(map(lambda x: parse_graph('data/graphs/data/' + x),
                '''skos.dot
generations.dot
travel.dot
univ-bench.dot
atom-primitive.dot
biomedical-mesure-primitive.dot
foaf.dot
people_pets.dot
funding.dot
wine.dot
pizza.dot'''.split('\n')))

        # q1
        right_q1 = list(map(int,'''810
                                2164
                                2499
                                2540
                                15454
                                15156
                                4118
                                9472
                                17634
                                66572
                                56195'''.split('\n')))
        Q1_hom = parse_grammar_hom('data/grammars/Q1_hom')
        Q1, eps_nonterminals_q1= parse_grammar('data/grammars/Q1')

        for graph, answer in zip(graphs,right_q1):
            res = trans_closure(graph[:], Q1_hom)
            self.assertEqual(len(list(filter(lambda x: x[1] =='S', res))), answer)

            res = bottom_up(graph[:], Q1, eps_nonterminals_q1)
            self.assertEqual(len(list(filter(lambda x: x[1] == 'S', res))), answer)

        # q2
        right_q2 = list(map(int,'''1
                                0
                                63
                                81
                                122
                                2871
                                10
                                37
                                1158
                                133
                                1262'''.split('\n')))

        Q2, eps_nonterminals_q2 = parse_grammar('data/grammars/Q2')
        Q2_hom = parse_grammar_hom('data/grammars/Q2_hom')

        for graph, answer in zip(graphs, right_q2):
            res = trans_closure(graph[:], Q2_hom)
            self.assertEqual(len(list(filter(lambda x: x[1] == 'S', res))), answer)
            res = bottom_up(graph[:], Q2, eps_nonterminals_q2)
            self.assertEqual(len(list(filter(lambda x: x[1] == 'S', res))), answer)



if __name__ == '__main__':
    unittest.main()

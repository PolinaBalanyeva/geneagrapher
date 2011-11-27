import unittest
from geneagrapher.graph import DuplicateNodeError, Graph, Node, Record


class TestGraphMethods(unittest.TestCase):
    """
    Unit tests for the Graph class.
    """
    def setUp(self):
        self.record1 = Record(u"Carl Friedrich Gau\xdf",
                              u"Universit\xe4t Helmstedt", 1799, 18231)
        self.node1 = Node(self.record1, set(), set())
        self.graph1 = Graph([self.node1])

    def test001_init_empty(self):
        # Test the constructor.
        graph = Graph()
        self.assertEquals(graph.seeds, None)

    def test002_init(self):
        # Test the constructor.
        self.assert_(self.graph1.seeds == [self.node1])
        self.assertEquals(self.graph1.keys(), [18231])
        self.assertEquals(self.graph1[18231], self.node1)

    def test003_init_bad_seeds(self):
        # Test the constructor when passed a bad type for the seeds parameter.
        self.assertRaises(TypeError, Graph, 3)

    def test004_has_node_true(self):
        # Test the has_node() method for a True case.
        self.assertEquals(self.graph1.has_node(18231), True)

    def test005_has_node_false(self):
        # Test the has_node() method for a False case.
        self.assertEquals(self.graph1.has_node(1), False)

    def test004_has_node_true(self):
        # Test the __contains__() method for a True case.
        self.assertEquals(18231 in self.graph1, True)

    def test005_has_node_false(self):
        # Test the __contains__() method for a False case.
        self.assertEquals(1 in self.graph1, False)

    def test006_get_node(self):
        # Test the get_node() method.
        node = self.graph1.get_node(18231)
        self.assert_(node == self.node1)

    def test007_get_node_not_found(self):
        # Test the get_node() method for a case where the node does not exist.
        self.assertRaises(KeyError, self.graph1.get_node, 1)

    def test008_get_node_list(self):
        # Test the get_node_list() method.
        self.assertEquals(self.graph1.get_node_list(), [18231])

    def test008_get_node_list_empty(self):
        # Test the get_node_list() method for an empty graph.
        graph = Graph()
        self.assertEquals(graph.get_node_list(), [])

    def test009_add_node(self):
        # Test the add_node() method.
        self.graph1.add_node("Leonhard Euler", "Universitaet Basel", 1726,
                             38586, set(), set())
        self.assertEquals([38586, 18231], self.graph1.get_node_list())
        self.assertEquals(self.graph1.seeds, [self.node1])

    def test010_add_second_node_seed(self):
        # Test the add_node() method when adding a second node and
        # marking it as a seed node.
        self.graph1.add_node("Leonhard Euler", "Universitaet Basel", 1726,
                             38586, set(), set(), True)
        self.assertEquals([38586, 18231], self.graph1.get_node_list())
        self.assertEquals(self.graph1.seeds, [self.node1,
                                              self.graph1.get_node(38586)])

    def test011_add_node_seed(self):
        # Test the add_node() method when no seeds exist.
        graph = Graph()
        self.assertEquals(graph.seeds, None)
        graph.add_node("Leonhard Euler", "Universitaet Basel", 1726,
                       38586, set(), set())
        self.assertEquals(graph.seeds, [graph.get_node(38586)])

    def test012_add_node_already_present(self):
        self.graph1.add_node("Leonhard Euler", "Universitaet Basel", 1726,
                             38586, set(), set())
        self.assertEquals([38586, 18231], self.graph1.get_node_list())
        self.assertRaises(DuplicateNodeError, self.graph1.add_node,
                          "Leonhard Euler", "Universitaet Basel",
                          1726, 38586, set(), set())

        try:
            self.graph1.add_node("Leonhard Euler", "Universitaet Basel",
                                 1726, 38586, set(), set())
        except DuplicateNodeError as e:
            self.assertEquals(str(e),
                              "node with id {} already exists".format(38586))
        else:
            self.fail()

    def test013_add_node_object(self):
        # Test the add_node_object() method.
        record = Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        node = Node(record, set(), set())
        self.graph1.add_node_object(node)
        self.assertEquals([38586, 18231], self.graph1.get_node_list())
        self.assertEquals(self.graph1.seeds, [self.node1])

    def test014_generate_dot_file(self):
        # Test the generate_dot_file() method.
        dotfileexpt = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    18231 [label="Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt (1799)"];

}
"""
        dotfile = self.graph1.generate_dot_file(True, False)
        self.assertEquals(dotfile, dotfileexpt)

    def test015_generate_dot_file(self):
        # Test the generate_dot_file() method.
        graph = Graph()
        graph.add_node(u"Carl Friedrich Gau\xdf", u"Universit\xe4t Helmstedt",
                       1799, 18231, set([18230]), set())
        graph.add_node(u"Johann Friedrich Pfaff",
                       u"Georg-August-Universit\xe4t Goettingen", 1786, 18230,
                       set([66476]), set())
        graph.add_node(u"Abraham Gotthelf Kaestner", u"Universit\xe4t Leipzig",
                       1739, 66476, set([57670]), set())
        graph.add_node(u"Christian August Hausen",
                       u"Martin-Luther-Universit\xe4t Halle-Wittenberg", 1713,
                       57670, set([72669]), set())
        graph.add_node(u"Johann Christoph Wichmannshausen",
                       u"Universit\xe4t Leipzig", 1685, 72669, set([21235]),
                       set())
        graph.add_node(u"Otto Mencke", u"Universit\xe4t Leipzig", 1665, 21235,
                       set(), set())

        dotfileexpt = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    18231 [label="Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt (1799)"];
    18230 [label="Johann Friedrich Pfaff \\nGeorg-August-Universit\xe4t \
Goettingen (1786)"];
    66476 [label="Abraham Gotthelf Kaestner \\nUniversit\xe4t Leipzig (1739)"];
    57670 [label="Christian August Hausen \\nMartin-Luther-Universit\xe4t \
Halle-Wittenberg (1713)"];
    72669 [label="Johann Christoph Wichmannshausen \\nUniversit\xe4t Leipzig \
(1685)"];
    21235 [label="Otto Mencke \\nUniversit\xe4t Leipzig (1665)"];

    18230 -> 18231;
    66476 -> 18230;
    57670 -> 66476;
    72669 -> 57670;
    21235 -> 72669;
}
"""
        dotfile = graph.generate_dot_file(True, False)
        self.assertEquals(dotfile, dotfileexpt)

if __name__ == '__main__':
    unittest.main()

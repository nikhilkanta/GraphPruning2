
import networkx as nx
import graphpruning2 as gp

def setUp():
    number_of_nodes = 100
    number_of_edges = 200
    Graph = nx.gnm_random_graph(number_of_nodes, number_of_edges)

def test_compute_significance():
    assert gp.compute_significance(G) == 0

def test_prune():
    number_of_edges_to_remove = number_of_edges / 2
    G_pruned = gp.prune(G, attribute_to_prune="significance", number_of_edges_to_remove=number_of_edges_to_remove)
    assert len(G_pruned.edges()) = number_of_edges / 2

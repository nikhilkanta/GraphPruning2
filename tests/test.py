
import networkx as nx
import graphpruning2 as gp
import random

def test_filter():
    number_of_nodes = 100
    number_of_edges = 200
    Graph = nx.gnm_random_graph(number_of_nodes, number_of_edges)
    Filter = gp.filter()
    number_of_edges_to_remove = number_of_edges // 2
    nx.set_edge_attributes(Graph, 0, 'weight')

    for edge_pair in Graph.edges():
        first_node, second_node = edge_pair
        Graph[first_node][second_node]['weight'] = random.randint(1, 10)
    Filter.compute_significance(Graph)
    G_pruned = Filter.prune(Graph,
                            attribute_to_prune="significance",
                            number_of_edges_to_remove=int(number_of_edges_to_remove))

    assert len(G_pruned.edges()) == number_of_edges / 2

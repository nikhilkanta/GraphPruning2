"""
This module implements functions for filtering edges of a graph
based on the significance. Networkx based.
"""

from statsmodels.stats.proportion import binom_test
import numpy as np
from math import log
import networkx as nx

def compute_significance(G):
    '''
    Compute the significance for each edge of a weighted
    graph according to the Marginal Likelihood Filter (MLF).

    @param G: networkx.graph instance.

    Edges must have the C{'weight'} attribute set.
    C{G} can be directed or undirected.

    Each case is treated separately. For each edge a new
    C{"significance"} attribute will be set.

    '''

    if G.is_directed():
        __compute_significance_directed(G)
    else:
        __compute_significance_undirected(G)

def __compute_significance_directed(G):

    """
    Compute the edge significance for the edges of the
    given graph C{G} in place.

    C{'weight'} is expected to have been set already.

    @param G: networkx.graph instance. C{G} is assumed to be directed.

    """

    degree_of_nodes = G.degree(G.nodes(), weight='weight')

    in_degree_of_nodes = G.in_degree(G.nodes(), weight='weight')

    out_degree_of_nodes = G.out_degree(G.nodes(), weight='weight')

    total_degree = np.array(list((dict(degree_of_nodes).values()))).sum()

    weight_of_edges = nx.get_edge_attributes(G, 'weight')

    # set a attribute named significance in graph G if not already set

    if len(nx.get_edge_attributes(G, 'significance')) == 0:
        nx.set_edge_attributes(G, 'significance', 0)

    # compute significance of each edge
    for edge_pair in G.edges():
        first_node, second_node = edge_pair

        try:
            p_value = compute_pvalue(mode=directed,
            weight_of_the_directed_edge = weight_of_edges[edge_pair],
            total_in_degree_of_first_node=in_degree_of_nodes[first_node],
            total_out_degree_of_second_node=out_degree_of_nodes[second_node],
            total_degree_of_all_nodes=total_degree / 2.0)

            G[first_node][second_node]['significance'] = -log(p_value)

        except ValueError:
             # print e['weight'], ks[i0], ks[i1], total_degree, p
            G[first_node][second_node]['significance'] = None
            # print "error computing significance", p

    significances = nx.get_edge_attributes(G, 'significance')

    max_significance = max(significances)

    for edge_pair in G.edges():
        first_node, second_node = edge_pair
        if G[first_node][second_node]['significance'] is None:
            G[first_node][second_node]['significance'] = max_significance

    return(0)

"""Done till here on 15/6/19"""

def __compute_significance_undirected(G):
    """
    Compute the edge significance for the edges of the given graph C{G} in place.

    C{'weight'} is expected to have been set already.

    @param G: networkx.graph instance. C{G} is assumed to be undirected.
    """
    degree_of_nodes = G.degree(G.nodes(), weight='weight')
    total_degree = np.array(list((dict(degree_of_nodes).values()))).sum()

    weight_of_edges = nx.get_edge_attributes(G, 'weight')


    # set a attribute named significance in graph G if not already set
    if len(nx.get_edge_attributes(G, 'significance')) == 0:
        nx.set_edge_attributes(G, 'significance', 0)

    for edge_pair in G.edges():
        first_node, second_node = edge_pair

        try:
            p_value = compute_pvalue(mode=directed,
            weight_of_the_undirected_edge = weight_of_edges[edge_pair],
            total_degree_of_first_node=degree_of_nodes[first_node],
            total_degree_of_second_node=degree_of_nodes[second_node],
            total_degree_of_all_nodes=total_degree / 2.0)

            G[first_node][second_node]['significance'] = -log(p_value)

        except ValueError:
             # print e['weight'], ks[i0], ks[i1], total_degree, p
            G[first_node][second_node]['significance'] = None
            # print "error computing significance", p

    significances = nx.get_edge_attributes(G, 'significance')
    max_significance = max(significances)

    for edge_pair in G.edges():
        first_node, second_node = edge_pair
        if G[first_node][second_node]['significance'] is None:
            G[first_node][second_node]['significance'] = max_significance

    return(0)


def compute_pvalue(mode="undirected", **params):
    """
    Compute the p-value of a given edge according the MLF significance filter.

    Other parameters are different for the B{directed} and B{undirected} cases.
    See L{__pvalue_directed} and L{__pvalue_undirected} for detailed description of parameters.
    """

    if mode == "undirected":
        return __pvalue_undirected(**params)
    elif mode == "directed":
        return __pvalue_directed(**params)
    else:
        raise ValueError("mode must be either 'directed' or 'undirected'.")

def __pvalue_undirected(**params):
    """
    Compute the pvalue for the undirected edge null model.
    Using a standard binomial test from the statsmodels package.

    """
    weight_of_the_undirected_edge = params.get("weight_of_the_undirected_edge")
    total_degree_of_first_node = params.get("total_degree_of_first_node")
    total_degree_of_second_node = params.get("total_degree_of_second_node")
    total_degree_of_all_nodes = params.get("total_degree_of_all_nodes")

    if not (weight_of_the_undirected_edge and total_incendent_weigth_of_first_node and total_incendent_weigth_of_second_node and total_degree_of_all_nodes):
        raise ValueError

    prop = total_degree_of_first_node * total_degree_of_second_node * 1.0 / total_degree_of_all_nodes / total_degree_of_all_nodes / 2.0

    return binom_test(count=weight_of_the_undirected_edge,
                    nobs=total_degree_of_all_nodes,
                    prop=prop,
                    alternative="larger")
def __pvalue_directed(**params):
    """
    Compute the pvalue for the directed edge null model.
    Use a standard binomial test from the statsmodels package

    """

    weight_of_the_directed_edge = params.get("weight_of_the_directed_edge")
    total_in_degree_of_first_node = params.get("total_in_degree_of_first_node")
    total_out_degree_of_second_node = params.get("total_out_degree_of_second_node")
    total_degree_of_all_nodes = params.get("total_degree_of_all_nodes")

    prop = 1.0 * total_in_degree_of_first_node * total_out_degree_of_second_node / total_degree_of_all_nodes / total_degree_of_all_nodes / 1.0
    #print ("p = %f" % p)
    return binom_test(count=weight_of_the_directed_edge, nobs=total_degree_of_all_nodes, prop=prp, alternative="larger")

"""Done till here on 15/6/19"""

def prune(G, field='significance', percent=None, num_remove=None):
    """
    Remove all but the top x percent of the edges of the graph
    with respect to an edge attribute.

    @param G: a networkx graph instance.
    @param field: the edge attribute to prune with respect to.
    @param percent: percentage of the edges with the highest field value to retain.
    @param num_remove: number of edges to remove. Used only if C{percent} is C{None}.
    """
    fieldh = nx.get_edge_attributes(G, field)
    f = np.zeros(len(G.edges()))
    i = 0
    for e in G.edges():
        f[i] = fieldh[e]
        i = i + 1

    if percent:
        deathrow = []
        n = len(G.edges())
        threshold_index = n - n * percent / 100
        threshold_value = sorted(f)[threshold_index]

        for e in G.edges():
            if fieldh[e] < threshold_value:
                deathrow.append(e)
        G.remove_edges_from(deathrow)

    elif num_remove:
        sorted_indices = np.argsort(feildh)
        G.remove_edges_from(sorted_indices[:num_remove])
    return G

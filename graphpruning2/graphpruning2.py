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
    total_degree = np.array(list((dict(degree_of_nodes).values()))).sum()

    weights_of_edges = nx.get_edge_attributes(G, 'weight')

    # set a attribute named significance in graph G if not already set
    if len(nx.get_edge_attributes(G, 'significance')) == 0:
        nx.set_edge_attributes(G, 'significance', 0)

    for edge_pair in G.edges():
        first_edge, second_edge = edge_pair

        try:
            p_value = compute_pvalue(weight_of_the_directed_edge = weights[edge_pair],
            total_incident_weight_of_first_node=degree_of_nodes[first_edge],
            total_incident_weight_of_second_node=degree_of_nodes[second_edge],
            total_incident_weight_of_all_nodes=total_degree / 2.0)

            G[first_edge][second_edge]['significance'] = -log(p_value)

        except ValueError:
             # print e['weight'], ks[i0], ks[i1], total_degree, p
            G[first_edge][second_edge]['significance'] = None
            # print "error computing significance", p

    significances = nx.get_edge_attributes(G, 'significance')
    max_significance = max(significances)

    for edge_pair in G.edges():
        first_edge, second_edge = edge_pair
        if G[first_edge][second_edge]['significance'] is None:
            G[first_edge][second_edge]['significance'] = max_significance

    return(0)

"""Done till here on 15/6/19"""

def __compute_significance_undirected(G):
    """
    Compute the edge significance for the edges of the
    given graph C{G} in place. C{'weight'} is expected
    to have been set already.
    @param G: networkx.graph instance. C{G} is assumed to be undirected.
    """
    ks = G.degree(G.nodes(), weight='weight')
    total_degree = 0
    for n in G.nodes():
        i = ks[n]
        total_degree = total_degree + i


    weights = nx.get_edge_attributes(G, 'weight')
    if len(nx.get_edge_attributes(G, 'significance')) == 0:
        nx.set_edge_attributes(G, 'significance', 0)
    for e in G.edges():
        i0, i1 = e

        try:
            p = pvalue(w = weights[e], ku=ks[i0], kv=ks[i1], q=total_degree / 2.0)
            G[i0][i1]['significance'] = -log(p)
        except ValueError:
             # print e['weight'], ks[i0], ks[i1], total_degree, p
            G[i0][i1]['significance'] = None

            # print "error computing significance", p
    significances = nx.get_edge_attributes(G, 'significance')
    max_sig = max(significances)
    for e in G.edges():
        i0, i1 = e
        if G[i0][i1]['significance'] is None:
            G[i0][i1]['significance'] = max_sig

def compute_pvalue(mode="undirected", **params):
    """
    Compute the p-value of a given edge according the MLF significance filter.

    @param mode: can be C{"directed"} or C{"undirected"}.
    @kwarg w: integer weight of the edge.
    @kwarg ku: weighted degree of one end node.
    @kwarg kv: weighted degree of the other end node.
    @kwarg q: sum of all weighted degrees in graph divided by 2.

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
    Use a standard binomial test from the statsmodels package.

    @keyword w: weight of the undirected edge.
    @keyword ku: total incident weight (strength) of the first node.
    @keyword kv: total incident weight (strength) of the second node.
    @keyword q: total incident weight of all nodes divided by two. Similar to the total number of edges in the graph.
    """
    weight_of_the_undirected_edge = params.get("w")
    total_incident_weight_of_first_node = params.get("ku")
    total_incident_weight_of_second_node = params.get("kv")
    total_incident_weight_of_all_nodes = params.get("q")

    if not (weight_of_the_undirected_edge and total_incendent_weigth_of_first_node and total_incendent_weigth_of_second_node and total_incident_weight_of_all_nodes):
        raise ValueError

    p = ku * kv * 1.0 / q / q / 2.0
    return binom_test(count=w, nobs=q, prop=p, alternative="larger")

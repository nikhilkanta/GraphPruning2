# GraphPruning2


<br/>

<div align="center">
  <!-- Python version -->
  <a href="https://pypi.python.org/pypi/graphpruning2">
    <img src="https://img.shields.io/badge/python-3.x-blue.svg?style=flat-square" alt="PyPI version"/>
  </a>
  <a href="https://pypi.org/project/graphpruning2/">
    <img src="https://badge.fury.io/py/graphpruning2.svg" alt="PyPI"/>
  </a>
  <!-- Build status -->
  <a href="https://travis-ci.org/nikhilkanta/GraphPruning2?branch=master">
    <img src="https://api.travis-ci.org/nikhilkanta/GraphPruning2.svg?branch=master&style=flat-square" alt="Build Status"/>
  </a>
  <!-- License -->
  <a href="https://opensource.org/licenses/MIT">
    <img src="http://img.shields.io/:license-mit-ff69b4.svg?style=flat-square" alt="license"/>
  </a>
</div>

<br/>

Networkx based Package for "pruning" weighted complex networks based on the Marginal Likelihood Filter.

# Overview
When dealing with weighted complex networks of dyadic relationships between nodes, we frequently encounter overly-dense "hairball" networks where the large number of edges may obfuscate the most important structures within the graph.

People often "prune" the graph by simply setting a threshold on the edge weights and removing all edges below the threshold. However, this simplistic approach systematically disfavours low-degree nodes and the structures they represent.Therefore, we need to measure the significance of an edge, with respect to the degrees of its incident vertices.

Here, we do this using a version of the configuration model as our null model that defines what we expect an edge’s weight to be given its end-nodes’ degrees. The null model predicts a probability distribution for the value of the edge weight. By comparing the observed weight of an edge with this predicted distribution, we can then compute a p-value which tells us how surprising the observed value is given the null model. This p-value gives us a measure of the statistical significance of the edge, and we can filter the edges according to this significance rather than the raw weight itself.

<<<<<<< HEAD

=======
- More: http://www.naviddianati.com/research
>>>>>>> 72e2efcdc5ebd0626774cbb9095e49cf15adaaa5
- Link to paper: http://journals.aps.org/pre/abstract/10.1103/PhysRevE.93.012304 (preprint: http://arxiv.org/abs/1503.04085)
- HTML version of paper: http://www.naviddianati.com/papers/graphpruning/html/manuscript.html

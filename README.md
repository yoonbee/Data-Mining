# Data-Mining

## Graph Data Mining

### DM6 - Graph Entropy
A protein-protein interaction data set is provided to discover sets of proteins densely connected each other. The densely connected proteins are likely to have the same cellular functions. Implement the Graph Entropy algorithm as a density-based graph clustering method. In Step-1, select the seed node of the highest degree among those which are not in any clusters previously determined, and form an initial cluster including the seed node and its neighbors. In Step-2, remove a neighbor of the seed iteratively in a decreasing order of degree if the removal of a neighbor decreases graph entropy. In Step-3, add a node on the outer boundary of the current cluster in a decreasing order of degree if the addition of the node decreases graph entropy. In an output file, show each cluster of size greater than 2 at each line in the format of the size and each protein in the cluster, for example, "3: {YBR160W YDR224C YPL231W}". Print the clusters in a decreasing order of their size.

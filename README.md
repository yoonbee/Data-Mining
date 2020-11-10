# Data-Mining

## Frequent Pattern Mining

### DM1 - Apriori algorithm
We can discover frequent gene sets from input data of functional categories and annotating genes. A frequent gene set means a set of genes that work for the same cellular functions frequently. Implement the Apriori algorithm to read the data set provided and find frequent gene sets with minimum support of 3.5%. Your program will print the frequent gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent gene set at each line, for example, {YAL005c, YBR044c} 3.8% support.


### DM2 - Charm algorithm
We can discover frequent closed gene sets from input data of functional categories and annotating genes. A frequent closed gene set means a set of genes frequently occurring in the same cellular functions, which does not have any super-set with the same support. Implement the Charm algorithm to read the data set provided and find frequent closed gene sets with minimum support of 3.5%. Your program will print the frequent closed gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent closed gene set at each line, for example, {YAL005c, YBR044c} 3.8% support

---
## Clustering

### DM3 - k-Means
A time-series gene expression data set is provided to discover gene sets with co-expression patterns (similar expressions during a given time range). The co-expressed genes are likely to have the same cellular functions. Implement k-Means with k=10 to find 10 clusters of genes. Use Euclidean distance to measure distance between data objects. In an output file, show each cluster at each line starting with the size of the cluster, for example, "6: {1, 24, 56, 139, 285, 471}".

### DM4 - DBSCAN
A time-series gene expression data set is provided to discover gene sets with co-expression patterns (similar expressions during a given time range). The co-expressed genes are likely to have the same cellular functions. Implement the DBSCAN algorithm as a density-based approach. Use Euclidean distance to measure distance between data points. Use epsilon = 1.0 and 2.0 and min_pts = 2, 4, and 6. In output files, show each cluster at each line starting with the size of the cluster, for example, "6: {1, 24, 56, 139, 285, 471}".

### DM5 - Comparing Accuracy of Clustering Results by Incident Matrices
A cluster validation algorithm assesses the quality of clustering results. Using the Jaccard index of two incident matrices of the output clusters and the ground-truth clusters, measure the accuracy of the clustering results from k-Means where k = 10 and DBSCAN where epsilon = 1.0 and 2.0 and min_pts = 2, 4, and 6. Your program will take two input files: one has the ground-truth clusters and the other is an output file on Assignment 3 or 4. Your program will print a Jaccard index value to the screen.

---
## Graph Data Mining

### DM6 - Graph Entropy
A protein-protein interaction data set is provided to discover sets of proteins densely connected each other. The densely connected proteins are likely to have the same cellular functions. Implement the Graph Entropy algorithm as a density-based graph clustering method. In Step-1, select the seed node of the highest degree among those which are not in any clusters previously determined, and form an initial cluster including the seed node and its neighbors. In Step-2, remove a neighbor of the seed iteratively in a decreasing order of degree if the removal of a neighbor decreases graph entropy. In Step-3, add a node on the outer boundary of the current cluster in a decreasing order of degree if the addition of the node decreases graph entropy. In an output file, show each cluster of size greater than 2 at each line in the format of the size and each protein in the cluster, for example, "3: {YBR160W YDR224C YPL231W}". Print the clusters in a decreasing order of their size.

---
## Project
Three categories of graph clustering algorithms have been discussed in class: density-based algorithms, partition-based algorithms, and hierarchical algorithms. Develop your own algorithm that is technically sound. When a protein-protein interaction network is used as input, the output clusters represent potential protein complexes. Justify that your own algorithm has competitive performance. Use the f-measure to evaluate the clustering results by comparing to protein complex data provided. Compute an f-score for each output cluster by selecting the maximum f-score to a protein complex, and average the f-scores of all output clusters. Compare the average f-scores between your algorithm and two previous algorithms implemented in Programming Assignments. If you have a team project, compare the algorithms using an additional cluster validation method for graph clustering. (But, do not use incident matrices.)

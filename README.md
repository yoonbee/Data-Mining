# Data-Mining

## Frequent Pattern Mining

### DM1 - Apriori algorithm
We can discover frequent gene sets from input data of functional categories and annotating genes. A frequent gene set means a set of genes that work for the same cellular functions frequently. Implement the Apriori algorithm to read the data set provided and find frequent gene sets with minimum support of 3.5%. Your program will print the frequent gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent gene set at each line, for example, {YAL005c, YBR044c} 3.8% support.


### DM2 - Charm algorithm
We can discover frequent closed gene sets from input data of functional categories and annotating genes. A frequent closed gene set means a set of genes frequently occurring in the same cellular functions, which does not have any super-set with the same support. Implement the Charm algorithm to read the data set provided and find frequent closed gene sets with minimum support of 3.5%. Your program will print the frequent closed gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent closed gene set at each line, for example, {YAL005c, YBR044c} 3.8% support

---
## Cluster

### DM3 - k-Means
A time-series gene expression data set is provided to discover gene sets with co-expression patterns (similar expressions during a given time range). The co-expressed genes are likely to have the same cellular functions. Implement k-Means with k=10 to find 10 clusters of genes. Use Euclidean distance to measure distance between data objects. In an output file, show each cluster at each line starting with the size of the cluster, for example, "6: {1, 24, 56, 139, 285, 471}".

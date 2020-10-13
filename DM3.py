"""
2018253015  YoonBee Kim     Assignment 3
"""

# Import NumPy to use arrays
import numpy as np

k = 10


# This function returns the Euclidean distance between two data points x and y
# param x: A data point
# param y: A data point
# return: The Euclidean distance between x and y
def distance(x, y):
    """
    FILL UP HERE!
    """
    # use Euclidean distance to measure the distance between two data points
    return np.sqrt(np.sum(pow(x - y, 2)))


# This function reads all data points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of data points
def get_input_data(filename):
    data = []
    with open(filename) as file:
        """
            FILL UP HERE!
        """
        # read each line and append to data
        for line in file:
            sp = line.strip().split('\t')
            data.append(sp)

    return np.array(data, dtype=float)


# This function creates k initial clusters by partitioning the input data sequentially with equal size
# param data: An array of data points
# return: An array of initial clusters
def generate_initial_clusters(data):
    clusters = []
    """
    FILL UP HERE!
    """
    # make 10 clusters which shape is (50, 12)
    clusters = data.reshape((k, int(len(data) / k), 12))
    return clusters


# This function calculates the mean points of the current set of clusters and return them in an array
# param clusters: An array of current clusters
# return: An array of mean points of the clusters
def calculate_means(clusters):
    means = []
    """
    FILL UP HERE!
    """
    # get the mean point of each cluster
    for cluster in clusters:
        sums = np.zeros((1, 12))
        for object in cluster:
            sums += object
        means.append(sums / len(cluster))
    return np.array(means)


# This function generates a new set of clusters by assigning each data point to the nearest mean point
# param means: An array of mean points
# param data: An array of data points
# return: An array of new clusters
def generate_new_clusters(means, data):
    clusters = [[] for _ in range(k)]
    """
    FILL UP HERE!
    """
    for row in data:
        dis = []
        # calculate the distance from the mean point of all clusters
        for i, mean in enumerate(means):
            dis.append(distance(row, mean))

        # assign each object to the nearest centroid and generate new clusters
        clusters[np.argmin(dis)].append(row)

    return clusters


# This function checks whether the new set of clusters have changed from the previous set of clusters
# param oldClusters: An array of the previous set of clusters
# param newClusters: An array of the new set of clusters
# return: the boolean value
def has_clusters_changed(oldClusters, newClusters):
    """
    FILL UP HERE!
    """
    # return false if clusters are same else return true
    for old, new in zip(oldClusters, newClusters):
        if np.array_equiv(old, new):
            return False
        else:
            return True

    return False


# This function implements the k-means algorithm by taking the input data
# It iteratively generates a new set of clusters until they do not change from the previous set of clusters
# param data: An array of data points
# return: An array of output clusters
def extract_kmean_clusters(data):
    old_clusters = generate_initial_clusters(data)
    means = calculate_means(old_clusters)
    new_clusters = generate_new_clusters(means, data)

    while has_clusters_changed(old_clusters, new_clusters):
        """
        FILL UP HERE!
        """
        # get mean points and make new clusters until there is no change of the object in each cluster
        old_clusters = new_clusters
        means = calculate_means(old_clusters)
        new_clusters = generate_new_clusters(means, data)

    return new_clusters


# This function writes the output clusters to a file, each cluster per line, following the format such as
# 4: { 1, 2, 5, 6 } where 4 is the total number of data points in the cluster
# and { 1, 2, 5, 6 } represents the row numbers (starting from 0) of the data points in the cluster
# param filename: The output filename
# param clusters: The output clusters
# param input_data: An array of input data points
def output_to_file(filename, clusters, input_data):
    file = open(filename, 'w')
    """
    FILL UP HERE!
    """
    # print out the length of each cluster and gene ID
    for cluster in clusters:
        s = str(len(cluster))+": {"
        for object in cluster:
            for i, data in enumerate(input_data):
                if np.array_equal(object, data):
                    s += str(i)+", "
        s = s[:-2] + "}\n"
        file.write(s)
    file.close()


# The main function
def main():
    input_filename = 'assignment3_input.txt'
    output_filename = 'result3.txt'
    genes = get_input_data(input_filename)
    gene_clusters = extract_kmean_clusters(genes)
    output_to_file(output_filename, gene_clusters, genes)


if __name__ == "__main__":
    main()

import math

epsilon = [1.0, 2.0]
min_pts = [2, 4, 6]


# This function reads all data points from the input file and returns them in an array
# param filename: The name of the input file
# return: An array of data points
def get_input_data(filename):
    data = []
    with open(filename) as file:
        # read each line and append to data
        for line in file:
            sp = list(map(float, line.strip().split('\t')))
            data.append(sp)

    return data


# This function returns the Euclidean distance between two data points x and y
# param x: A data point
# param y: A data point
# return: The Euclidean distance between x and y
def distance(x, y):
    sum = 0
    for x1, y1 in zip(x, y):
        sum += pow(x1 - y1, 2)
    return math.sqrt(sum)


# This function find all the reachable points from data_points
# param data: An array of data points
# param data_points: An array of data points which have to find a reachable points
# param cluster: An array of the cluster
# param epsilon: Minimum radius of neighborhood
# param min_pts: Minimum number of data points of an e-neighborhood
# return: cluster of data_points
def find_all_reachable_data_points(data, data_points, cluster, epsilon, min_pts):
    for data_point in data_points:

        reachable_points = []
        cnt = 0

        for d in data:
            # calculates distances from all data
            if distance(data_point, d) <= epsilon:
                cnt += 1
                if d not in cluster:
                    cluster.append(d)
                    if distance(data_point, d) != 0:
                        reachable_points.append(d)

        # if data_point is a border
        if cnt < min_pts:
            return cluster

        # if data_point is a core, retrieve all data points
        else:
            find_all_reachable_data_points(data, reachable_points, cluster, epsilon, min_pts)

    return cluster


# This function selects a data point and get a cluster
# param data: An array of data points
# param epsilon: Minimum radius of neighborhood
# param min_pts: Minimum number of data points of an e-neighborhood
# return: clusters of data_points
def extract_DBSCAN_clusters(data, epsilon, min_pts):
    clusters = []

    for data_point in data:
        flag = False

        # skip to next data_point if data_point already included in cluster
        for cluster in clusters:
            if data_point in cluster:
                flag = True
                break

        if flag is False:
            new_cluster = find_all_reachable_data_points(data, [data_point], [], epsilon, min_pts)
            if new_cluster is not None:
                clusters.append(new_cluster)

    return clusters


# This function writes the output clusters to a file, each cluster per line, following the format such as
# 4: { 1, 2, 5, 6 } where 4 is the total number of data points in the cluster
# and { 1, 2, 5, 6 } represents the row numbers (starting from 0) of the data points in the cluster
# param filename: The output filename
# param clusters: The output clusters
# param input_data: An array of input data points
def output_to_file(filename, clusters, input_data):
    file = open(filename, 'w')
    for cluster in clusters:
        s = str(len(cluster))+": {"
        for i, data in enumerate(input_data):
            if data in cluster:
                for c in cluster:
                    if c == data:
                        s += str(i)+", "
        s = s[:-2]+"}\n"
        file.write(s)
    file.close()


# The main function
def main():
    input_filename = 'assignment4_input.txt'
    genes = get_input_data(input_filename)
    for e in epsilon:
        for m in min_pts:
            gene_clusters = extract_DBSCAN_clusters(genes, e, m)

            # sort clusters by size of a cluster
            gene_clusters.sort(key=lambda size: len(size), reverse=True)

            # file name includes of epsilon and min_pts
            output_filename = 'result_' + str(e) + '_' + str(m) + '.txt'
            output_to_file(output_filename, gene_clusters, genes)


if __name__ == "__main__":
    main()

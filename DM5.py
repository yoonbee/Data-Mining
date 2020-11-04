"""
2018253015 Yoon Bee, Kim
"""


# This function return clusters from ground truth file
# param filename: ground truth file name
# return: clusters of ground truth file
def get_ground_truth_clusters(filename):
    clusters = []
    outliers = []

    with open(filename) as file:
        for i, line in enumerate(file):
            sp = line.strip().split('\t')

            # outlier
            if int(sp[0]) == -1:
                outliers.append(i)
                continue

            if len(clusters) == int(sp[0]) - 1:
                clusters.append([])

            clusters[int(sp[0]) - 1].append(i)

    for outlier in outliers:
        clusters.append([outlier])

    return clusters


# This function return clusters from output file
# param filename: output file name
# return: clusters of output file
def get_output_clusters(filename):
    clusters = []

    with open(filename) as file:
        for line in file:
            sp = line.replace(':', '').replace('{', '').replace('}', '').replace(',', '').strip().split(' ')
            clusters.append(list(map(int, sp[1:])))

    return clusters


# This function get incident matrix of all data
# param size_of_data: total data size
# param clusters: clusters of data
# return: incident matrix of all data
def get_incident_matrix(size_of_data, clusters):
    incident_matrix = [[0 for j in range(i)] for i in range(size_of_data)]

    for cluster in clusters:
        for d1 in cluster:
            for d2 in range(d1):
                if d2 in cluster:
                    incident_matrix[d1][d2] = 1

    return incident_matrix


# This function get jaccard index of ground truth incident matrix and output incident matrix
# param ground_truth_incident_matrix: incident matrix of ground truth
# param output_incident_matrix: incident matrix of output
# return: jaccard index of ground truth incident matrix and output incident matrix
def get_jaccard_index(ground_truth_incident_matrix, output_incident_matrix):
    diff = 0
    both_1 = 0

    for row_g, row_o in zip(ground_truth_incident_matrix, output_incident_matrix):
        for col_g, col_o in zip(row_g, row_o):
            if col_g == 1 and col_o == 1:
                both_1 += 1
            elif col_g == 0 and col_o == 0:
                continue
            else:
                diff += 1

    return both_1 / (both_1 + diff)


# This function writes the jaccard index to file
# param output_file: list of output file name
# param jaccard_index: jaccard index of ground truth incident matrix and output incident matrix
def output_to_file(output_file, jaccard_index):
    with open('result5.txt', 'w') as file:
        for output, jaccard in zip(output_file, jaccard_index):
            s = output + "'s jaccard: " + str(jaccard) + '\n'
            file.write(s)


# The main function
def main():
    size_of_data = 500
    ground_truth_file = 'assignment5_input.txt'
    output_file = ['result3.txt']
    for e in [1.0, 2.0]:
        for m in [2, 4, 6]:
            output_file.append('result_' + str(e) + '_' + str(m) + '.txt')

    jaccard_index = []

    ground_truth_clusters = get_ground_truth_clusters(ground_truth_file)
    ground_truth_incident_matrix = get_incident_matrix(size_of_data, ground_truth_clusters)

    for output in output_file:
        output_clusters = get_output_clusters(output)
        output_incident_matrix = get_incident_matrix(size_of_data, output_clusters)

        # get jaccard index
        jaccard_index.append(get_jaccard_index(ground_truth_incident_matrix, output_incident_matrix))

    output_to_file(output_file, jaccard_index)


if __name__ == "__main__":
    main()

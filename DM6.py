import copy
import math


# This function reads data set and return graph
# param filename: The name of the input file
# return: dictionary(key: vertex & value: list of neighbor vertex
def get_input_data(filename):
    graph = dict()

    with open(filename) as file:
        for line in file:
            sp = line.replace('-', '').strip().split('\t')

            for s in sp:
                if s not in graph:
                    graph[s] = []

            graph[sp[0]].append(sp[1])
            graph[sp[1]].append(sp[0])

    return graph


# This function return the seed node which is the highest degree
# param graph: dictionary(key: vertex & value: list of neighbor vertex
# return: seed node which has the highest degree
def select_seed_node(graph):
    seed = ""
    highest_degree = 0

    for g_key, g_value in graph.items():
        if highest_degree <= len(g_value):
            seed = g_key
            highest_degree = len(g_value)

    return seed


# This function get a vertex entropy
# param inner, outer: number or inner and outer
# return: vertex entropy
def get_vertex_entropy(inner, outer):
    if inner == 0 or outer == 0:
        return 0.0
    return -inner / (inner + outer) * math.log2(inner / (inner + outer)) - outer / (inner + outer) * math.log2(
        outer / (inner + outer))


# This function get a graph entropy
# param check: list of vertex which entropy will be change
# param cluster: seed cluster to check it is inner links or outer links
# param graph: dictionary(key: vertex & value: list of neighbor vertex
# return: graph entropy
def get_graph_entropy(check, cluster, graph):
    entropy = 0.0

    for c in check:
        inner = 0
        outer = 0

        for vertex in graph[c]:
            if vertex in cluster:
                inner += 1
            else:
                outer += 1

        entropy += get_vertex_entropy(inner, outer)

    return entropy


# This function remove neighbors if removal of neighbor decrease entropy
# param seed: seed node
# param cluster: initial cluster(seed node, neighbors of seed node)
# return: cluster which have the smallest entropy(after removal of neighbors)
# return: smallest entropy
def get_seed_cluster(seed, cluster, graph):
    # sort neighbor with degree
    graph[seed].sort(key=lambda x: len(graph[x]), reverse=True)

    for neighbor in graph[seed]:
        # find all the vertex which entropy will be change
        check = copy.deepcopy(graph[neighbor])
        check.append(neighbor)

        # entropy before removal of neighbor
        entropy = get_graph_entropy(check, cluster, graph)

        # remove neighbor of seed cluster
        new_cluster = copy.deepcopy(cluster)
        new_cluster.remove(neighbor)

        # entropy after removal of neighbor
        new_entropy = get_graph_entropy(check, new_cluster, graph)

        # if entropy decreases then remove neighbor
        if new_entropy < entropy:
            cluster = new_cluster
            entropy = new_entropy

    return cluster, entropy


# This function get list of outer boundary of cluster
# param cluster: current cluster which have the smallest entropy
# return: list of outer boundary sorted by degree
def get_outer_boundary(cluster, graph):
    outer_boundary = set()

    for vertex in cluster:
        outer_boundary.update(graph[vertex])

    return sorted(list(outer_boundary - set(cluster)), key=lambda x: len(graph[x]), reverse=True)


# This function add outer boundary to cluster if addition of outer boundary node increase entropy
# param outer_boundary: list of outer boundary sorted by degree
# cluster: current cluster which have the smallest entropy
# return: cluster which have the smallest entropy(after addition of outer boundary)
# return: smallest entropy
def add_outer_boundary(outer_boundary, cluster, graph):
    for outer in outer_boundary:
        # find all the vertex which entropy will be change
        check = copy.deepcopy(graph[outer])
        check.append(outer)

        # entropy before addition of outer boundary
        entropy = get_graph_entropy(check, cluster, graph)

        # add outer boundary of current cluster
        new_cluster = copy.deepcopy(cluster)
        new_cluster.append(outer)

        # entropy after addition of outer boundary
        new_entropy = get_graph_entropy(check, new_cluster, graph)

        # if entropy decreases then add outer boundary
        if new_entropy <= entropy:
            cluster = new_cluster

    return cluster


# This function apply graph entropy algorithm
# param graph: dictionary(key: vertex & value: list of neighbor vertex
def apply_graph_entropy_algorithm(graph):
    clusters = []

    graph_k = copy.deepcopy(graph)

    while graph_k:
        # step 1 - get a seed node and form initial cluster
        seed_node = select_seed_node(graph_k)

        initial_cluster = copy.deepcopy(graph[seed_node])
        initial_cluster.append(seed_node)

        # step 2 - remove a neighbor of seed if removal of neighbor decreases entropy
        cluster, entropy = get_seed_cluster(seed_node, initial_cluster, graph)

        # step 3 - add outer boundary to cluster if addition of outer boundary increases entropy
        while True:
            outer_boundary = get_outer_boundary(cluster, graph)
            new_cluster = add_outer_boundary(outer_boundary, cluster, graph)

            # if cluster doesn't change then finish
            if cluster == new_cluster:
                break

            cluster = new_cluster

        for vertex in cluster:
            if vertex in graph_k:
                del graph_k[vertex]

        clusters.append(cluster)

    return clusters


# This function writes the output clusters to a file
# param filename: The output filename
# param clusters: The output clusters
def output_to_file(filename, clusters):
    file = open(filename, 'w')

    for cluster in clusters:
        if len(cluster) <= 2:
            continue

        s = str(len(cluster)) + ": {"
        for c in cluster:
            s += c + " "
        s = s[:-1] + "} \n"
        file.write(s)

    file.close()


def main():
    input_filename = 'assignment6_input.txt'
    output_filename = 'result6.txt'
    graph = get_input_data(input_filename)

    clusters = apply_graph_entropy_algorithm(graph)
    clusters.sort(key=lambda x: len(x), reverse=True)

    output_to_file(output_filename, clusters)


if __name__ == "__main__":
    main()

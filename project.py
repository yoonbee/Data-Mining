import copy
import math
import time


def get_input_data():
    with open('project_input.txt') as file:
        graph = dict()

        for line in file:
            sp = line.replace('-', '').strip().split('\t')

            for s in sp:
                if s not in graph:
                    graph[s] = []

            graph[sp[0]].append(sp[1])
            graph[sp[1]].append(sp[0])

    return graph


def get_ground_truth_data():
    with open('ground_truth.txt') as file:
        ground_truth = []

        for line in file:
            sp = line.replace('-', '').strip().split(' ')
            ground_truth.append(sp)

    return ground_truth


def select_seed_node(graph):
    seed = ""
    highest_degree = 0

    for g_key, g_value in graph.items():
        if highest_degree <= len(g_value):
            seed = g_key
            highest_degree = len(g_value)

    return seed


def get_weight(v1, v2, graph, option_weight):
    if option_weight == 'cn':
        return len(set(graph[v1]) & set(graph[v2])) / (len(set(graph[v1]) | set(graph[v2])))


def get_vertex_entropy(inner, outer, weight_inner, weight_outer, option_method):
    if weight_inner == 0.0 or weight_outer == 0.0:
        return 0.0

    elif option_method == 'wrge':
        return -weight_inner / (weight_inner + weight_outer) * math.log2(weight_inner / (weight_inner + weight_outer)) \
               - weight_outer / (weight_inner + weight_outer) * math.log2(weight_outer / (weight_inner + weight_outer))

    elif option_method == 'mwge':
        if inner == 0 or outer == 0:
            return 0.0
        else:
            return -weight_inner * inner / (inner + outer) * math.log2(inner / (inner + outer)) \
                   - weight_outer * outer / (inner + outer) * math.log2(outer / (inner + outer))


def get_graph_entropy(check, cluster, graph, option_method, option_weight):
    entropy = 0.0

    for c in check:
        inner = 0
        outer = 0
        weight_inner = 0.0
        weight_outer = 0.0

        for vertex in graph[c]:
            if vertex in cluster:
                inner += 1
                weight_inner += get_weight(c, vertex, graph, option_weight)

            else:
                outer += 1
                weight_outer += get_weight(c, vertex, graph, option_weight)

        entropy += get_vertex_entropy(inner, outer, weight_inner, weight_outer, option_method)

    return entropy


def get_seed_cluster(seed, cluster, graph, option_method, option_weight):
    # sort neighbor with degree
    graph[seed].sort(key=lambda x: len(graph[x]), reverse=True)

    for neighbor in graph[seed]:
        # find all the vertex which entropy will be change
        check = copy.deepcopy(graph[neighbor])

        # entropy before removal of neighbor
        entropy = get_graph_entropy(check, cluster, graph, option_method, option_weight)

        # remove neighbor of seed cluster
        new_cluster = copy.deepcopy(cluster)
        new_cluster.remove(neighbor)

        # entropy after removal of neighbor
        new_entropy = get_graph_entropy(check, new_cluster, graph, option_method, option_weight)

        # if entropy decreases then remove neighbor
        if new_entropy < entropy:
            cluster = new_cluster
            entropy = new_entropy

    return cluster, entropy


def get_outer_boundary(cluster, graph):
    outer_boundary = set()

    for vertex in cluster:
        outer_boundary.update(graph[vertex])

    return sorted(list(outer_boundary - set(cluster)), key=lambda x: len(graph[x]), reverse=True)


def add_outer_boundary(outer_boundary, cluster, graph, option_method, option_weight):
    for outer in outer_boundary:
        # find all the vertex which entropy will be change
        check = copy.deepcopy(graph[outer])

        # entropy before addition of outer boundary
        entropy = get_graph_entropy(check, cluster, graph, option_method, option_weight)

        # add outer boundary of current cluster
        new_cluster = copy.deepcopy(cluster)
        new_cluster.append(outer)

        # entropy after addition of outer boundary
        new_entropy = get_graph_entropy(check, new_cluster, graph, option_method, option_weight)

        # if entropy decreases then add outer boundary
        if new_entropy <= entropy:
            cluster = new_cluster

    return cluster


def apply_graph_entropy_algorithm(graph, option_method, option_weight):
    clusters = []

    graph_k = copy.deepcopy(graph)

    while graph_k:
        # step 1 - get a seed node and form initial cluster
        seed_node = select_seed_node(graph_k)

        initial_cluster = copy.deepcopy(graph[seed_node])
        initial_cluster.append(seed_node)

        # step 2 - remove a neighbor of seed if removal of neighbor decreases entropy
        cluster, entropy = get_seed_cluster(seed_node, initial_cluster, graph, option_method, option_weight)

        # step 3 - add outer boundary to cluster if addition of outer boundary increases entropy
        while True:
            outer_boundary = get_outer_boundary(cluster, graph)
            new_cluster = add_outer_boundary(outer_boundary, cluster, graph, option_method, option_weight)

            # if cluster doesn't change then finish
            if cluster == new_cluster:
                break

            cluster = new_cluster

        for vertex in cluster:
            if vertex in graph_k:
                del graph_k[vertex]

        clusters.append(cluster)

    return clusters


def get_validation_score(clusters, ground_truth, option_validation):
    if option_validation == 'f-measure':
        sum = 0.0

        for cluster in clusters:
            highest_f_measure = 0.0

            if len(cluster) == 1:
                continue

            for gt in ground_truth:
                recall = len(set(cluster) | set(gt)) / len(gt)
                precision = len(set(cluster) | set(gt)) / len(cluster)
                f_measure = 2 * recall * precision / (recall + precision)

                if highest_f_measure <= f_measure:
                    highest_f_measure = f_measure

            sum += highest_f_measure

        return sum/len(clusters)
    # TODO: aupr 코드 짜기
    # elif option_validation == 'aupr':


def WRGE(option_weight, option_validation):
    graph = get_input_data()
    ground_truth = get_ground_truth_data()
    clusters = apply_graph_entropy_algorithm(graph, 'wrge', option_weight)
    score = get_validation_score(clusters, ground_truth, option_validation)
    print("method: WRGE / weight:", option_weight, "/ validation:", option_validation, "/ score:", score)


def MWGE(option_weight, option_validation):
    graph = get_input_data()
    ground_truth = get_ground_truth_data()
    clusters = apply_graph_entropy_algorithm(graph, 'mwge', option_weight)
    score = get_validation_score(clusters, ground_truth, option_validation)
    print("method: MWGE / weight:", option_weight, "/ validation:", option_validation, "/ score:", score)


def main():
    # WRGE('cn', 'f-measure')
    # WRGE('cn', 'aupr')

    # MWGE('cn', 'f-measure')
    # MWGE('cn', 'aupr')


if __name__ == "__main__":
    main()

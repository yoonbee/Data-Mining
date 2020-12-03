import copy
import time


# This function reads data set and return graph
# param filename: The name of the input file
# return: dictionary(key: vertex & value: list of neighbor vertex
def get_input_data(filename):
    with open(filename) as file:
        graph = dict()

        for line in file:
            sp = line.replace('-', '').strip().split('\t')

            for s in sp:
                if s not in graph:
                    graph[s] = set()

            graph[sp[0]].update([sp[1]])
            graph[sp[1]].update([sp[0]])

    return graph


def find_all_the_subgraphs(graph):
    subgraphs = []

    for key in graph.keys():
        s = set([key])
        s.update(graph[key])
        subgraphs.append(s)

    result_subgraphs = []
    remain_graph = subgraphs

    while True:
        if len(remain_graph) == 0:
            break

        s1 = remain_graph.pop()

        tmp_set = set(s1)
        while True:
            if len(s1) == 0:
                break

            s2 = s1.pop()

            for set_list in remain_graph:
                if s2 in set_list:
                    for ver in set_list:
                        if ver not in tmp_set:
                            s1.add(ver)
                    tmp_set.update(set_list)
                    remain_graph.remove(set_list)

        result_subgraphs.append(tmp_set.copy())

    return result_subgraphs


# This
def get_density(subgraph, graph):
    num_of_edeg = 0

    for v1 in subgraph:
        for v2 in subgraph:
            if v1 == v2:
                continue
            if v2 in graph[v1]:
                num_of_edeg += 1

    return num_of_edeg / (len(subgraph) * (len(subgraph) - 1))


def get_jaccard_index(e1, e2):
    return len(e1 & e2) / len(e1 | e2)


def find_smallest_jaccard_edge(graph):
    smallest_jaccard = len(graph.keys())
    edge = []

    for v1 in graph.keys():
        for v2 in graph[v1]:
            jaccard_index = get_jaccard_index(set(graph[v1]), set(graph[v2]))

            if jaccard_index < smallest_jaccard:
                smallest_jaccard = jaccard_index
                edge = [v1, v2]

    return edge


def apply_hierarchical_algorithm(graph):
    clusters = []
    subgraphs = find_all_the_subgraphs(graph)

    while len(subgraphs) != 0:
        subgraph = subgraphs.pop()
        print(len(subgraphs), subgraph)

        density = get_density(subgraph, graph)

        if density >= 0.5:
            for vertex in subgraph:
                del graph[vertex]

            for key in graph.keys():
                if vertex in graph[key]:
                    graph[key].remove(vertex)

            clusters.append(subgraph)
        else:
            subgraph_copy = copy.deepcopy(subgraph)
            sub_graph = dict()

            for vertex in subgraph:
                sub_graph[vertex] = graph[vertex]

            while True:
                cnt_sub = len(find_all_the_subgraphs(sub_graph))
                target_edge = find_smallest_jaccard_edge(sub_graph)

                sub_graph[target_edge[0]].remove(target_edge[1])
                sub_graph[target_edge[1]].remove(target_edge[0])

                if len(sub_graph[target_edge[0]]) == 0:
                    del sub_graph[target_edge[0]]
                    subgraph.remove(target_edge[0])

                if len(sub_graph[target_edge[1]]) == 0:
                    del sub_graph[target_edge[1]]
                    subgraph.remove(target_edge[1])

                if len(sub_graph.keys()) == 0:
                    clusters.append(subgraph_copy)
                    break
                if cnt_sub != len(find_all_the_subgraphs(sub_graph)):
                    sub = find_all_the_subgraphs(sub_graph)
                    subgraphs.extend(sub)
                    break

    return clusters


# This function writes the output clusters to a file
# param filename: The output filename
# param clusters: The output clusters
def output_to_file(filename, clusters):
    file = open(filename, 'w')

    for cluster in clusters:
        if len(cluster) < 2:
            continue

        s = str(len(cluster)) + ": {"
        for c in cluster:
            s += c + " "
        s = s[:-1] + "} \n"
        file.write(s)

    file.close()


def main():
    st = time.time()
    input_filename = 'assignment7_input.txt'
    output_filename = 'result7.txt'

    graph = get_input_data(input_filename)
    clusters = apply_hierarchical_algorithm(graph)
    clusters.sort(key=lambda x: len(x), reverse=True)

    output_to_file(output_filename, clusters)


if __name__ == "__main__":
    main()

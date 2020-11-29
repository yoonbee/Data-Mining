import copy
import time


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


    return subgraphs


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

    # for subgraph in copy.deepcopy(subgraphs):
    #     density = get_density(subgraph, graph)
    #
    #     if density >= 0.5:
    #         for vertex in subgraph:
    #             del graph[vertex]
    #
    #         for key in graph.keys():
    #             if vertex in graph[key]:
    #                 graph[key].remove(vertex)
    #
    #         clusters.append(subgraph)
    #         subgraphs.remove(subgraph)
    #
    # for k, v in graph.items():
    #     print(k, len(v), v)
    # for subgraph in subgraphs:
    #     print(subgraph)
    #     sub_dict = dict()
    #
    #     for vertex in subgraph:
    #         sub_dict[vertex] = graph[vertex]
    #
    # #
    # #     # while True:
    # #         # cnt_sub = len(find_all_the_subgraphs(sub_dict))
    #     target_edge = find_smallest_jaccard_edge(sub_dict)
    #     print(target_edge)


def main():
    st = time.time()
    input_filename = 'assignment7_input.txt'
    graph = get_input_data(input_filename)

    clusters = apply_hierarchical_algorithm(graph)
    # print(time.time()-st)


if __name__ == "__main__":
    main()

# Day 25: Snowverload
import collections as coll
import copy
import os
import pathlib

from adventofcode.algorithm import algo


def part_one(graph):
    answer_1 = solve_alternative_1(copy.deepcopy(graph), 3)
    answer_2 = solve_alternative_2(copy.deepcopy(graph), 3)
    assert answer_1 == answer_2
    print(f"Part one: {answer_1}")


def parse(file_path):
    graph = coll.defaultdict(list)
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            node, neighbors = line.split(": ")
            neighbors = neighbors.split(" ")
            for n in neighbors:
                graph[node].append(n)
                graph[n].append(node)
    return graph


def solve_alternative_1(graph, min_cut):
    edges = algo.rose_min_cut(graph)
    assert len(edges) == min_cut
    for a, b in edges:
        graph[a].remove(b)
        graph[b].remove(a)
    a, b = edges[0]
    partition_a = set(algo.flood_fill(graph, a, neighbor_generator))
    partition_b = set(algo.flood_fill(graph, b, neighbor_generator))
    return len(partition_a) * len(partition_b)


def neighbor_generator(graph, _, node):
    for n in graph[node]:
        yield n


def solve_alternative_2(graph, min_cut):
    while True:
        new_graph = copy.deepcopy(graph)
        cut = algo.kargers_algorithm(new_graph)
        if cut == min_cut:
            a, b = new_graph.keys()
            return (len(a) // 3) * (len(b) // 3)


def main():
    graph = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(graph))


if __name__ == "__main__":
    main()

# Day 10: Pipe Maze
import copy
import os
import pathlib

from adventofcode.algorithm import algo


def part_one(graph, start):
    distances = algo.flood_fill(graph, start)
    answer = max(distances.values())
    print(f"Part one: {answer}")


def part_two(graph, start):
    distances = algo.flood_fill(graph, start)
    graph = {node: neighbors for node, neighbors in graph.items() if node in distances}
    y_range = get_extended_range([e[0] for e in graph.keys()])
    x_range = get_extended_range([e[1] for e in graph.keys()])
    insides = algo.get_insides(graph, y_range, x_range)
    answer = len(insides)
    print_graph(graph, insides, y_range, x_range)
    print(f"Part two: {answer}")


def parse(file_path):
    graph = {}
    start = None
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                node = (y, x)
                if char == ".":
                    continue
                if char == "S":
                    start = node
                else:
                    graph[node] = {  # Get the neighbors depending on type of node.
                        "|": ((y - 1, x), (y + 1, x)),
                        "-": ((y, x - 1), (y, x + 1)),
                        "L": ((y - 1, x), (y, x + 1)),
                        "J": ((y - 1, x), (y, x - 1)),
                        "7": ((y + 1, x), (y, x - 1)),
                        "F": ((y + 1, x), (y, x + 1)),
                    }[char]
    assert start is not None
    graph[start] = get_start_neighbors(graph, start)
    return graph, start


def get_start_neighbors(graph, start):
    start_neighbors = []
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor == start:
                start_neighbors.append(node)
    assert len(start_neighbors) == 2
    return tuple(start_neighbors)


def get_extended_range(values):
    return (min(values) - 1, max(values) + 2)


def print_graph(graph, inside, y_range, x_range):
    for y in range(*y_range):
        line = ""
        for x in range(*x_range):
            node = (y, x)
            if node in graph:
                line += "#"
            elif node in inside:
                line += "I"
            else:
                line += "."
        print(line)


def main():
    graph, start = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(graph), copy.deepcopy(start))
    part_two(copy.deepcopy(graph), copy.deepcopy(start))


if __name__ == "__main__":
    main()

# Day 11: Cosmic Expansion
import copy
import pathlib
import os


def part_one(nodes):
    nodes = expand_nodes(nodes, 1)
    answer = find_distance_between_all_pairs(nodes)
    print(f"Part one: {answer}")


def part_two(nodes):
    nodes = expand_nodes(nodes, 1000000 - 1)
    answer = find_distance_between_all_pairs(nodes)
    print(f"Part two: {answer}")


def parse(file_path):
    nodes = []
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                if char == "#":
                    nodes.append((y, x))
    return nodes


def expand_nodes(nodes, expansion):
    occupied_rows = set(e[0] for e in nodes)
    occupied_cols = set(e[1] for e in nodes)
    y_limit = max(e[0] for e in nodes)
    x_limit = max(e[1] for e in nodes)
    new_nodes = copy.deepcopy(nodes)
    for y in range(0, y_limit + 1):
        if y not in occupied_rows:
            new_nodes = [
                new if old[0] < y else (new[0] + expansion, new[1])
                for old, new in zip(nodes, new_nodes)
            ]
    for x in range(0, x_limit + 1):
        if x not in occupied_cols:
            new_nodes = [
                new if old[1] < x else (new[0], new[1] + expansion)
                for old, new in zip(nodes, new_nodes)
            ]
    return new_nodes


def find_distance_between_all_pairs(nodes):
    distance = 0
    for i, node in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            distance += manhattan_distance(node, nodes[j])
    return distance


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def main():
    nodes = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(nodes))
    part_two(copy.deepcopy(nodes))


if __name__ == "__main__":
    main()

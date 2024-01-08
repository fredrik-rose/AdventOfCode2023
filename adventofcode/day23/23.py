# Day 23: A Long Walk
import copy
import os
import pathlib
import sys

from adventofcode.algorithm import algo


sys.setrecursionlimit(15000)


def part_one(grid, start, end):
    def generate_neighbors(graph, node):
        next_nodes = set()
        if graph[node] == "<":
            next_nodes.add(node - 1)
        elif graph[node] == ">":
            next_nodes.add(node + 1)
        elif graph[node] == "^":
            next_nodes.add(node - 1j)
        elif graph[node] == "v":
            next_nodes.add(node + 1j)
        else:
            assert graph[node] == "."
            next_nodes.update(get_neighbors(grid, node))
        for n in next_nodes:
            if n in graph:
                yield n, 1

    answer = algo.longest_path(grid, start, end, generate_neighbors)
    print(f"Part one: {answer}")


def part_two(grid, start, end):
    graph = algo.compress_maze(grid, start, end, get_neighbors)
    answer = algo.longest_path(graph, start, end, lambda graph, node: graph[node])
    print(f"Part two: {answer}")


def parse(file_path):
    grid = {}
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                if char == "#":
                    continue
                node = x + y * 1j
                grid[node] = char
    start = list(grid.keys())[0]
    end = list(grid.keys())[-1]
    return grid, start, end


def get_neighbors(grid, position):
    neighbors = set()
    for y in (-1, 1):
        neighbors.add(position + (y * 1j))
    for x in (-1, 1):
        neighbors.add(position + x)
    neighbors = [e for e in neighbors if e in grid]
    return neighbors


def main():
    grid, start, end = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid), start, end)
    part_two(copy.deepcopy(grid), start, end)


if __name__ == "__main__":
    main()

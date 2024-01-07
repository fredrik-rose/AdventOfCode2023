# Day 21: Step Counter
import collections as coll
import copy
import os
import pathlib

from adventofcode.algorithm import algo


def part_one(grid, start):
    ends = walk(grid, start, 64)
    answer = len(ends)
    print(f"Part one: {answer}")


def part_two(grid, start):
    grid_size = int(max(max(e.real, e.imag) for e in grid) + 1)
    half_grid_size = grid_size // 2
    grid = expand_grid(grid, grid_size, 5)
    start += (grid_size * 2) + (grid_size * 2j)
    x_s = (half_grid_size, half_grid_size + grid_size, half_grid_size + grid_size * 2)
    points = []
    for x in x_s:
        y = len(walk(grid, start, x))
        points.append((x, y))
    polynomial = algo.lagrange_polynomial(points)
    answer = int(polynomial(26501365))
    print(f"Part two: {answer}")


def parse(file_path):
    grid = set()
    start = None
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for x, char in enumerate(line):
                node = x + y * 1j
                if char == ".":
                    grid.add(node)
                elif char == "S":
                    grid.add(node)
                    start = node
                else:
                    assert char == "#"
    assert start is not None
    return grid, start


def walk(grid, start, length):
    queue = coll.deque([(0, start)])
    visited = set()
    ends = set()
    while queue:
        distance, node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        if distance > length:
            continue
        if (distance % 2) == (length % 2):
            ends.add(node)
        for n in generate_neighbors(grid, node):
            queue.append((distance + 1, n))
    return ends


def generate_neighbors(grid, node):
    neighbors = set()
    for y in (-1, 1):
        neighbors.add(node + (0 + y * 1j))
    for x in (-1, 1):
        neighbors.add(node + (x + 0j))
    for n in neighbors:
        if n in grid:
            yield n


def expand_grid(grid, size, n):
    new_grid = set()
    for y in range(n):
        for x in range(n):
            for node in grid:
                new_grid.add(node + (x * size + (y * size) * 1j))
    return new_grid


def main():
    grid, start = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid), copy.deepcopy(start))
    part_two(copy.deepcopy(grid), copy.deepcopy(start))


if __name__ == "__main__":
    main()

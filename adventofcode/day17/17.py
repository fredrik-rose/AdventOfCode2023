# Day 17: Clumsy Crucible
import copy
import functools
import os
import pathlib

from adventofcode.algorithm import algo


UP = 0 + -1j
DOWN = 0 + 1j
LEFT = -1 + 0j
RIGHT = 1 + 0j


def part_one(grid):
    answer = solve(grid, 0, 3)
    print(f"Part one: {answer}")


def part_two(grid):
    answer = solve(grid, 4, 10)
    print(f"Part two: {answer}")


def parse(file_path):
    grid = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            grid.append([int(e) for e in line])
    return grid


def solve(grid, min_steps, max_steps):
    start = ((0, 0), (0, 0))  # node, direction
    end = (len(grid[0]) - 1, len(grid) - 1)
    costs = algo.dijkstra(
        grid,
        start,
        functools.partial(neighbor_generator, min_steps=min_steps, max_steps=max_steps),
    )
    return min(c for node, c in costs.items() if node[0] == end)


def neighbor_generator(graph, node, min_steps, max_steps):
    node, direction = node
    node = pair_to_complex(node)
    direction = pair_to_complex(direction)
    for d in (UP, DOWN, LEFT, RIGHT):
        if d == direction:
            continue  # Must turn.
        if d == direction * -1:
            continue  # Can't go back.
        next_node = node
        cost = 0
        for i in range(max_steps):
            # Walk the allowed amount of steps in the current direction so that
            # we must turn at each node. By doing this we don't need to keep
            # track of the max allowed steps in a certain direction.
            next_node += d
            if not (
                0 <= next_node.imag < len(graph) and 0 <= next_node.real < len(graph[0])
            ):
                break
            cost += graph[int(next_node.imag)][int(next_node.real)]
            if (i + 1) < min_steps:
                continue
            yield ((complex_to_pair(next_node), complex_to_pair(d)), cost)


def complex_to_pair(number):
    return (number.real, number.imag)


def pair_to_complex(pair):
    return pair[0] + pair[1] * 1j


def main():
    grid = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid))
    part_two(copy.deepcopy(grid))


if __name__ == "__main__":
    main()

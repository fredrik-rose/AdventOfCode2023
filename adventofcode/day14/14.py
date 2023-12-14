# Day 14: Parabolic Reflector Dish
import copy
import os
import pathlib

from adventofcode.algorithm import algo


def part_one(grid):
    roll(grid)
    answer = north_load(grid)
    print(f"Part one: {answer}")


def part_two(grid):
    grid = run(grid, 1_000_000_000)
    answer = north_load(grid)
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        return [list(line.strip()) for line in file]


def run(grid, steps):
    grid_states = {}
    t = 0
    while t < steps:
        t += 1
        grid = spin(grid)
        state = "".join(algo.flatten_list(grid))
        if state in grid_states:
            cycle_length = t - grid_states[state]
            num_cycles = (steps - t) // cycle_length
            t += num_cycles * cycle_length
        else:
            grid_states[state] = t
    return grid


def spin(grid):
    for _ in range(4):
        roll(grid)
        grid = algo.rotate_clockwise(grid)
    return grid


def roll(grid):
    while True:
        change = False
        for y, (first, second) in enumerate(zip(grid[:-1], grid[1:])):
            for x, (a, b) in enumerate(zip(first, second)):
                if b == "O" and a == ".":
                    grid[y][x] = "O"
                    grid[y + 1][x] = "."
                    change = True
        if not change:
            break


def north_load(grid):
    result = 0
    for i, line in enumerate(grid[::-1]):
        result += sum(1 for e in line if e == "O") * (i + 1)
    return result


def main():
    grid = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid))
    part_two(copy.deepcopy(grid))


if __name__ == "__main__":
    main()

# Day 18: Lavaduct Lagoon
import copy
import os
import pathlib

import matplotlib.pyplot as plt

from adventofcode.algorithm import algo


def part_one(plan):
    answer = solve(plan)
    print(f"Part one: {answer}")


def part_two(plan):
    plan = translate_plan(plan)
    answer = solve(plan)
    print(f"Part two: {answer}")


def parse(file_path):
    plan = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            direction, length, color = line.split()
            length = int(length)
            color = color[1:-1]
            plan.append((direction, length, color))
    return plan


def solve(plan):
    polygon = get_polygon(plan)
    result = algo.polygon_internal_points(polygon) + algo.polygon_num_border_points(
        polygon
    )
    plt.plot([e[1] for e in polygon], [e[0] for e in polygon], "-*")
    plt.show()
    return int(result)


def translate_plan(plan):
    new_plan = []
    for direction, length, color in plan:
        length = int(color[1:-1], 16)
        direction = {
            0: "R",
            1: "D",
            2: "L",
            3: "U",
        }[int(color[-1])]
        new_plan.append((direction, length, color))
    return new_plan


def get_polygon(plan):
    polygon = [(0, 0)]
    for direction, length, _ in plan:
        prev = polygon[-1]
        if direction == "R":
            new = (prev[0], prev[1] + length)
        elif direction == "L":
            new = (prev[0], prev[1] - length)
        elif direction == "U":
            new = (prev[0] - length, prev[1])
        elif direction == "D":
            new = (prev[0] + length, prev[1])
        else:
            assert False
        polygon.append(new)
    return polygon


def main():
    plan = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(plan))
    part_two(copy.deepcopy(plan))


if __name__ == "__main__":
    main()

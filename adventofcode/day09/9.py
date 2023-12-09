# Day 9: Mirage Maintenance
import copy
import re

import numpy as np


def part_one(data):
    answer = 0
    for values in data:
        answer += get_next_number(values)
    print(f"Part one: {answer}")


def part_two(data):
    answer = 0
    for values in data:
        answer += get_next_number(values[::-1])
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        return [extract_ints(line.strip()) for line in file]


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def get_next_number(values):
    if not any(values):
        return 0
    return values[-1] + get_next_number(np.diff(values))


def main():
    data = parse("input.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


if __name__ == "__main__":
    main()

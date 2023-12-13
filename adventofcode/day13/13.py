# Day 13: Point of Incidence
import copy
import math
import os
import pathlib

from adventofcode.algorithm import algo


def part_one(boards):
    answer = solve(boards, 0)
    print(f"Part one: {answer}")


def part_two(boards):
    answer = solve(boards, 1)
    print(f"Part two: {answer}")


def parse(file_path):
    boards = []
    with open(file_path) as file:
        raw_boards = file.read().split("\n\n")
        for board in raw_boards:
            boards.append([line.strip() for line in board.strip().split("\n")])
    return boards


def solve(boards, max_diff):
    return (sum_mirror_lines(boards, max_diff) * 100) + sum_mirror_lines(
        [algo.rotate_clockwise(e) for e in boards], max_diff
    )


def sum_mirror_lines(boards, max_diff):
    return sum(
        math.ceil(x) for e in boards if (x := find_mirror_line(e, max_diff)) is not None
    )


def find_mirror_line(board, max_diff):
    for i in range(len(board) - 1):
        if count_mirror_errors(board, i, i + 1) == max_diff:
            return i + 0.5
    return None


def count_mirror_errors(board, row_a, row_b):
    return sum(
        algo.hamming_distance(a, b) for a, b in zip(board[row_a::-1], board[row_b:])
    )


def main():
    boards = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(boards))
    part_two(copy.deepcopy(boards))


if __name__ == "__main__":
    main()

# Day 24: Never Tell Me The Odds
import copy
import dataclasses
import os
import pathlib
import re

import z3

from adventofcode.algorithm import algo


@dataclasses.dataclass
class Hail:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


@dataclasses.dataclass
class LineSegment:
    xs: int
    ys: int
    xe: int
    ye: int


def part_one(hails):
    start = 200000000000000
    end = 400000000000000
    lines = get_line_segments(hails)
    answer = 0
    for i, a in enumerate(lines):
        j = i + 1
        for b in lines[j:]:
            intersection = algo.line_intersection(
                a.xs, a.ys, a.xe, a.ye, b.xs, b.ys, b.xe, b.ye
            )
            if intersection is not None:
                if start <= intersection[0] <= end and start <= intersection[1] <= end:
                    answer += 1
    print(f"Part one: {answer}")


def part_two(hails):
    x = z3.Int("x")
    y = z3.Int("y")
    z = z3.Int("z")
    vx = z3.Int("vx")
    vy = z3.Int("vy")
    vz = z3.Int("vz")
    solver = z3.Solver()
    for i, h in enumerate(hails):
        t = z3.Int(f"t{i}")
        solver.add(t >= 0)
        solver.add(x + t * vx == h.x + t * h.vx)
        solver.add(y + t * vy == h.y + t * h.vy)
        solver.add(z + t * vz == h.z + t * h.vz)
    assert str(solver.check()) == "sat"
    answer = solver.model().eval(x + y + z)
    print(f"Part two: {answer}")


def parse(file_path):
    hails = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            hails.append(Hail(*extract_ints(line)))
    return hails


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def get_line_segments(hails):
    lines = []
    for h in hails:
        xs = h.x
        ys = h.y
        xe = h.x + 1e16 * h.vx
        ye = h.y + 1e16 * h.vy
        lines.append(LineSegment(xs, ys, xe, ye))
    return lines


def main():
    hails = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(hails))
    part_two(copy.deepcopy(hails))


if __name__ == "__main__":
    main()

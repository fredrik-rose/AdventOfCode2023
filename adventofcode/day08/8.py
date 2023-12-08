# Day 8: Haunted Wasteland
import collections as coll
import functools
import math


def part_one(directions, graph):
    node = "AAA"
    answer = 0
    while node != "ZZZ":
        node = graph[node][directions[0]]
        directions.rotate(-1)
        answer += 1
    print(f"Part one: {answer}")


def part_two(directions, graph):
    nodes = [e for e in graph.keys() if e.endswith("A")]
    distances = []
    for node in nodes:
        distance = 0
        while not node.endswith("Z"):
            node = graph[node][directions[distance % len(directions)]]
            distance += 1
        distances.append(distance)
    answer = functools.reduce(lcm, distances)
    print(f"Part two: {answer}")


def parse(file_path):
    graph = {}
    with open(file_path) as file:
        directions = coll.deque(0 if e == "L" else 1 for e in file.readline().strip())
        file.readline()
        for line in file:
            line = line.strip()
            node, neighbors = line.split(" = ")
            left, right = neighbors.split(", ")
            assert node not in graph
            graph[node] = (left[1:], right[:-1])
    return directions, graph


def lcm(a, b):
    # Least-common multiplier.
    return int(a * b / math.gcd(a, b))


def main():
    directions, graph = parse("input.txt")
    part_one(directions.copy(), graph.copy())
    part_two(directions.copy(), graph.copy())


if __name__ == "__main__":
    main()

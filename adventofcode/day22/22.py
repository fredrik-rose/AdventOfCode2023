# Day 22: Sand Slabs
import collections as coll
import copy
import dataclasses
import os
import pathlib


@dataclasses.dataclass
class Coord:
    x: int
    y: int
    z: int


def part_one(blocks):
    graph = simulate(blocks)
    not_removable = set(
        list(support)[0] for support in graph.values() if len(support) == 1
    )
    removable = set(graph.keys()).difference(not_removable)
    answer = len(removable)
    print(f"Part one: {answer}")


def part_two(blocks):
    supported_by = simulate(blocks)
    supports = coll.defaultdict(set)
    for node, support in supported_by.items():
        for n in support:
            supports[n].add(node)
    answer = sum(bfs(supported_by, supports, i + 1) for i in range(len(blocks)))
    print(f"Part two: {answer}")


def parse(file_path):
    blocks = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            start, end = line.split("~")
            start = [int(e) for e in start.split(",")]
            end = [int(e) for e in end.split(",")]
            assert all(e >= 0 for e in start)
            assert all(e >= 0 for e in end)
            assert all(e >= s for s, e in zip(start, end))
            blocks.append([Coord(*start), Coord(*end)])
    return blocks


def simulate(blocks):
    size_x = max(e[1].x for e in blocks)
    size_y = max(e[1].y for e in blocks)
    blocks = sorted(blocks, key=lambda x: x[0].z)
    z_buffer = [[(0, 0) for x in range(size_x + 1)] for y in range(size_y + 1)]
    graph = coll.defaultdict(set)
    for i, brick in enumerate(blocks):
        node = i + 1
        max_z, graph[node] = find_z_buffer_top(z_buffer, brick)
        assert brick[0].z > max_z
        max_z += 1
        diff = brick[0].z - max_z
        brick[0].z -= diff
        brick[1].z -= diff
        update_z_buffer(z_buffer, brick, node)
    return graph


def find_z_buffer_top(z_buffer, brick):
    nodes = set()
    max_z = 0
    for y in range(brick[0].y, brick[1].y + 1):
        for x in range(brick[0].x, brick[1].x + 1):
            z, n = z_buffer[y][x]
            if z > max_z:
                max_z = z
                nodes.clear()
            if z == max_z:
                nodes.add(n)
    return max_z, nodes


def update_z_buffer(z_buffer, brick, node):
    for y in range(brick[0].y, brick[1].y + 1):
        for x in range(brick[0].x, brick[1].x + 1):
            z_buffer[y][x] = (brick[1].z, node)


def bfs(supported_by, supports, node):
    queue = coll.deque([node])
    visited = set()
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for n in supports[node]:
            if not supported_by[n].difference(visited):
                queue.append(n)
    return len(visited) - 1


def main():
    blocks = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(blocks))
    part_two(copy.deepcopy(blocks))


if __name__ == "__main__":
    main()

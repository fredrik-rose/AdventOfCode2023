# Day 16: The Floor Will Be Lava
import copy
import os
import pathlib


UP = 0 + -1j
DOWN = 0 + 1j
LEFT = -1 + 0j
RIGHT = 1 + 0j


def part_one(grid):
    visited = walk(grid, 0 + 0j, RIGHT)
    answer = get_energy(visited)
    print(f"Part one: {answer}")


def part_two(grid):
    energies = []
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for position, direction in ((0 + y * 1j, RIGHT), ((width - 1) + y * 1j, LEFT)):
            visited = walk(grid, position, direction)
            energy = get_energy(visited)
            energies.append(energy)
    for x in range(width):
        for position, direction in ((x + 0j, DOWN), (x + (height - 1) * 1j, UP)):
            visited = walk(grid, position, direction)
            energy = get_energy(visited)
            energies.append(energy)
    answer = max(energies)
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        return [list(line.strip()) for line in file]


def walk(grid, position, direction, visited=None):
    visited = visited if visited else set()
    while 0 <= position.imag < len(grid) and 0 <= position.real < len(grid[0]):
        state = (position, direction)
        if state in visited:
            return visited
        visited.add(state)
        element = grid[int(position.imag)][int(position.real)]
        if element == "/":
            direction = -direction.imag + -direction.real * 1j
        elif element == "\\":
            direction = direction.imag + direction.real * 1j
        elif element == "|" and direction.real:
            walk(grid, position + UP, UP, visited)
            direction = DOWN
        elif element == "-" and direction.imag:
            walk(grid, position + RIGHT, RIGHT, visited)
            direction = LEFT
        position += direction
    return visited


def get_energy(visited):
    return len(set(e[0] for e in visited))


def main():
    grid = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(grid))
    part_two(copy.deepcopy(grid))


if __name__ == "__main__":
    main()

# Day 6: Wait For It
import math
import re


def part_one(time, distance):
    answer = 1
    for t, d in zip(time, distance):
        answer *= get_number_of_winners(t, d)
    print(f"Part one: {answer}")


def part_two(time, distance):
    time = int("".join(str(e) for e in time))
    distance = int("".join(str(e) for e in distance))
    answer = get_number_of_winners(time, distance)
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        time = extract_ints(file.readline().strip())
        distance = extract_ints(file.readline().strip())
        return time, distance


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def get_number_of_winners(time, distance):
    # x^2 - Tx + D = 0
    x1, x2 = solve_quadratic_equation(1, -time, distance)
    x1 = math.ceil(x1)
    x2 = math.floor(x2)
    return x2 - x1 + 1


def solve_quadratic_equation(a, b, c):
    # ax^2 + bx + c = 0
    x1 = (-b - math.sqrt((b**2) - (4 * a * c))) / (2 * a)
    x2 = (-b + math.sqrt((b**2) - (4 * a * c))) / (2 * a)
    return x1, x2


def main():
    time, distance = parse("input.txt")
    part_one(time.copy(), distance.copy())
    part_two(time.copy(), distance.copy())


if __name__ == "__main__":
    main()

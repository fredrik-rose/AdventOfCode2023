# Day 12: Hot Springs
import copy
import os
import pathlib


DP = {}


def part_one(data):
    answer = 0
    for springs, rule in data:
        DP.clear()
        answer += count(springs, rule)
    print(f"Part one: {answer}")


def part_two(data):
    answer = 0
    for springs, rule in data:
        DP.clear()
        answer += count(((springs + ["?"]) * 5)[:-1], rule * 5)
    print(f"Part two: {answer}")


def parse(file_path):
    data = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            springs, rule = line.split()
            springs = list(springs)
            rule = [int(e) for e in rule.split(",")]
            data.append((springs, rule))
    return data


def count(springs, rules, group=0):
    if not springs and not rules:
        return 1 if group == 0 else 0
    if not springs and rules:
        return 1 if len(rules) == 1 and group == rules[0] else 0
    if not valid(rules, group):
        # Backtrack
        return 0
    current = springs[0]
    state = (current, len(springs), len(rules), group)
    if state in DP:
        # Dynamic programming
        return DP[state]
    if current == "#":
        result = count(springs[1:], rules, group + 1)
    if current == ".":
        if group > 0:
            if group != rules[0]:
                return 0
            result = count(springs[1:], rules[1:], 0)
        else:
            result = count(springs[1:], rules, 0)
    if current == "?":
        result = count(["."] + springs[1:], rules, group) + count(
            ["#"] + springs[1:], rules, group
        )
    DP[state] = result
    return result


def valid(rules, group):
    if not rules:
        return group == 0
    if group > rules[0]:
        return False
    return True


def main():
    data = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


if __name__ == "__main__":
    main()

# Day 19: Aplenty
import copy
import functools
import operator
import os
import pathlib
import re


def part_one(rules, parts):
    answer = sum(sum(part.values()) for part in parts if is_accepted(part, rules))
    print(f"Part one: {answer}")


def part_two(rules):
    ranges = {key: (1, 4001) for key in "xmas"}
    answer = walk_tree(rules, ranges, "in")
    print(f"Part two: {answer}")


def parse(file_path):
    rules = {}
    parts = []
    with open(file_path) as file:
        workflow_text, part_text = file.read().split("\n\n")
        for line in workflow_text.split():
            line = line.strip()
            match = re.search(r"(?P<name>[a-z]+)\{(?P<rules>.*)\}", line).groupdict()
            rules[match["name"]] = parse_rules(match["rules"])
        for line in part_text.split():
            line = line.strip()
            parts.append(parse_part(line))
    return rules, parts


def parse_rules(text):
    text_rules = text.split(",")
    rules = []
    for e in text_rules[:-1]:
        match = re.search(
            r"(?P<part>[a-z]+)(?P<operator>\<|\>)(?P<number>\d+):(?P<destination>[a-z,A-Z]+)",
            e,
        ).groupdict()
        rules.append(
            (
                match["part"],
                match["operator"],
                int(match["number"]),
                match["destination"],
            )
        )
    rules.append(text_rules[-1])
    return rules


def parse_part(text):
    text_sub_parts = text[1:-1].split(",")
    parts = {}
    for e in text_sub_parts:
        name, number = e.split("=")
        parts[name] = int(number)
    return parts


def is_accepted(part, rules):
    current = "in"
    while current not in ("A", "R"):
        for rule in rules[current][:-1]:
            op = operator.lt if rule[1] == "<" else operator.gt
            if op(part[rule[0]], rule[2]):
                current = rule[3]
                break
        else:
            current = rules[current][-1]
    return current == "A"


def walk_tree(rules, ranges, node):
    if node == "A":
        return range_product(ranges)
    if node == "R":
        return 0
    ranges_complement = dict(ranges)
    result = 0
    for part, op, number, destination in rules[node][:-1]:
        if op == ">":
            ranges[part] = range_intersection(ranges[part], (number + 1, 4001))
            ranges_complement[part] = range_intersection(
                ranges_complement[part], (1, number + 1)
            )
            result += walk_tree(rules, ranges, destination)
        elif op == "<":
            ranges[part] = range_intersection(ranges[part], (1, number))
            ranges_complement[part] = range_intersection(
                ranges_complement[part], (number, 4001)
            )
            result += walk_tree(rules, ranges, destination)
        else:
            assert False
        ranges = dict(ranges_complement)
    result += walk_tree(rules, ranges, rules[node][-1])
    return result


def range_intersection(a, b):
    return (max(a[0], b[0]), min(a[1], b[1]))


def range_product(ranges):
    return functools.reduce(
        lambda x, y: x * y, (max(e[1] - e[0], 0) for e in ranges.values())
    )


def main():
    rules, parts = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(rules), copy.deepcopy(parts))
    part_two(copy.deepcopy(rules))


if __name__ == "__main__":
    main()

# Day 15: Lens Library
import collections as coll
import copy
import os
import pathlib
import re


def part_one(instructions):
    answer = sum(calculate_hash(e) for e in instructions)
    print(f"Part one: {answer}")


def part_two(instructions):
    boxes = coll.defaultdict(dict)
    for element in instructions:
        label, operation, focal_length = parse_instruction(element)
        box_id = calculate_hash(label)
        if operation == "-":
            boxes[box_id].pop(label, None)
        elif operation == "=":
            boxes[box_id][label] = focal_length
        else:
            assert False
    answer = calclulate_focus_power(boxes)
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        return file.readline().strip().split(",")


def calculate_hash(string):
    result = 0
    for char in string:
        result += ord(char)
        result *= 17
        result = result % 256
    return result


def parse_instruction(instruction):
    instruction = re.search(
        r"(?P<label>[a-z]+)(?P<operation>=|-)(?P<focal_length>\d?)", instruction
    ).groupdict()
    return instruction["label"], instruction["operation"], instruction["focal_length"]


def calclulate_focus_power(boxes):
    result = 0
    for box, lenses in boxes.items():
        for i, focal_length in enumerate(lenses.values()):
            result += (box + 1) * (i + 1) * int(focal_length)
    return result


def main():
    instructions = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(instructions))
    part_two(copy.deepcopy(instructions))


if __name__ == "__main__":
    main()

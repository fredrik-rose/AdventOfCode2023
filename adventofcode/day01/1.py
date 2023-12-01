# Day 1: Trebuchet?!
import regex


def part_one(calibration):
    answer = solve(calibration, r"\d")
    print(f"Part one: {answer}")


def part_two(calibration):
    answer = solve(calibration, r"\d|one|two|three|four|five|six|seven|eight|nine")
    print(f"Part two: {answer}")


def parse(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file]


def solve(calibration, pattern):
    solution = 0
    for line in calibration:
        digits = [str_to_int(x) for x in regex.findall(pattern, line, overlapped=True)]
        number = int(f"{digits[0]}{digits[-1]}")
        solution += number
    return solution


def str_to_int(text):
    try:
        return int(text)
    except ValueError:
        return {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }[text]


def main():
    calibration = parse("input.txt")
    part_one(calibration.copy())
    part_two(calibration.copy())


if __name__ == "__main__":
    main()

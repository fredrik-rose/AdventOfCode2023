# Day 3: Gear Ratios
import collections as coll
import re


def part_one(numbers, symbols):
    part_numbers = get_part_numbers(numbers, symbols)
    answer = sum(sum(parts) for parts in part_numbers)
    print(f"Part one: {answer}")


def part_two(numbers, symbols):
    part_numbers = get_part_numbers(numbers, symbols, symbol_filter="*")
    answer = sum(parts[0] * parts[1] for parts in part_numbers if len(parts) == 2)
    print(f"Part two: {answer}")


def get_part_numbers(numbers, symbols, symbol_filter=None):
    symbol_positions = set(
        e[1] for e in symbols if symbol_filter is None or e[0] == symbol_filter
    )
    part_numbers = coll.defaultdict(list)  # {symbol_position: [neighbor_part_numbers]}
    for number, coordinates in numbers:
        for position in coordinates:
            for neighbor in generate_neighbor_positions(position):
                if neighbor in symbol_positions:
                    part_numbers[neighbor].append(number)
                    break
            else:
                continue
            break
    return list(part_numbers.values())


def generate_neighbor_positions(position):
    for y in range(-1, 2):
        for x in range(-1, 2):
            yield position + (x + y * 1j)


def parse(file_path):
    numbers = []
    symbols = []
    with open(file_path) as file:
        for y, line in enumerate(file):
            line = line.strip()
            for match in re.finditer(r"\d+", line):
                part_number = int(match.group())
                coordinates = [x + y * 1j for x in range(*match.span())]
                numbers.append((part_number, coordinates))
            for x, e in enumerate(line):
                if not e.isdigit() and e != ".":
                    symbols.append((e, x + y * 1j))
    return numbers, symbols


def main():
    numbers, symbols = parse("input.txt")
    part_one(numbers.copy(), symbols.copy())
    part_two(numbers.copy(), symbols.copy())


if __name__ == "__main__":
    main()

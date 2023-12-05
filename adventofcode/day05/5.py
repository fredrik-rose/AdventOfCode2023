# Day 5: If You Give A Seed A Fertilizer
import dataclasses
import re


@dataclasses.dataclass
class Mapper:
    dst: int
    src: int
    length: int


@dataclasses.dataclass
class Interval:
    start: int
    end: int

    def split(self, mapper):
        split = []
        if self.start >= mapper.src + mapper.length or self.end < mapper.src:
            return [self]
        if self.start < mapper.src:
            split.append(Interval(self.start, mapper.src))
        if self.end >= mapper.src + mapper.length:
            split.append(Interval(mapper.src + mapper.length, self.end))
        start = max(mapper.src, self.start)
        end = min(mapper.src + mapper.length - 1, self.end)
        split.append(Interval(start, end))
        return split


def part_one(seeds, maps):
    answer = min(convert_interval(Interval(s, s), maps)[0].start for s in seeds)
    print(f"Part one: {answer}")


def part_two(seeds, maps):
    converted_intervals = [
        convert_interval(Interval(first, first + second - 1), maps)
        for first, second in zip(seeds[0::2], seeds[1::2])
    ]
    answer = min(e.start for interval in converted_intervals for e in interval)
    print(f"Part two: {answer}")


def parse(file_path):
    maps = []
    with open(file_path) as file:
        seeds = extract_ints(file.readline())
        file.readline()
        for mapper in file.read().strip().split("\n\n"):
            maps.append([Mapper(*extract_ints(e)) for e in mapper.split("\n")[1:]])
        return seeds, maps


def extract_ints(text):
    return [int(x) for x in re.findall(r"-?\d+", text)]


def convert_interval(interval, maps):
    result = [interval]
    for converter in maps:
        next_result = []
        for converted_interval in result:
            splited_interval = split_interval(converted_interval, converter)
            next_result += [map_interval(e, converter) for e in splited_interval]
        result = next_result
    return result


def split_interval(interval, converter):
    split = [interval]
    for mapper in converter:
        next_split = []
        for cut_interval in split:
            next_split += cut_interval.split(mapper)
        split = next_split
    return split


def map_interval(interval, converter):
    for mapper in converter:
        if mapper.src <= interval.start < mapper.src + mapper.length:
            assert interval.end < mapper.src + mapper.length
            start = mapper.dst + (interval.start - mapper.src)
            end = mapper.dst + (interval.end - mapper.src)
            return Interval(start, end)
    return interval


def main():
    seeds, maps = parse("input.txt")
    part_one(seeds.copy(), maps.copy())
    part_two(seeds.copy(), maps.copy())


if __name__ == "__main__":
    main()

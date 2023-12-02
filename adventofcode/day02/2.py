# Day 2: Cube Conundrum


def part_one(game):
    answer = 0
    for game_id, sets in game.items():
        if all(s["red"] <= 12 and s["green"] <= 13 and s["blue"] <= 14 for s in sets):
            answer += game_id
    print(f"Part one: {answer}")


def part_two(game):
    answer = 0
    for sets in game.values():
        power = 1
        for color in ("red", "green", "blue"):
            power *= max(s[color] for s in sets)
        answer += power
    print(f"Part two: {answer}")


def parse(file_path):
    game = {}
    with open(file_path) as file:
        for line in file:
            raw_game_id, raw_game_sets = line.split(":")
            game_id = int(raw_game_id.split(" ")[1])
            game[game_id] = []
            for game_set in raw_game_sets.split(";"):
                single_set = {"red": 0, "green": 0, "blue": 0}
                for cube in game_set.split(","):
                    count, color = cube.strip().split(" ")
                    single_set[color] = int(count)
                game[game_id].append(single_set)
    return game


def main():
    game = parse("input.txt")
    part_one(game.copy())
    part_two(game.copy())


if __name__ == "__main__":
    main()

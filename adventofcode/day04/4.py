# Day 4: Scratchcards
import re


def part_one(cards):
    answer = 0
    for winners, numbers in cards.values():
        winners_count = get_number_of_winning_numbers(winners, numbers)
        if winners_count > 0:
            answer += 2 ** (winners_count - 1)
    print(f"Part one: {answer}")


def part_two(cards):
    card_counts = {card_id: 1 for card_id in cards.keys()}
    for card_id, (winners, numbers) in sorted(cards.items()):
        winners_count = get_number_of_winning_numbers(winners, numbers)
        for i in range(winners_count):
            try:
                card_counts[card_id + (i + 1)] += card_counts[card_id]
            except KeyError:
                continue
    answer = sum(card_counts.values())
    print(f"Part two: {answer}")


def parse(file_path):
    cards = {}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            match = re.search(
                r"Card\s+(?P<id>\d+):\s+(?P<winners>.*)\s+\|\s+(?P<numbers>.*)", line
            ).groupdict()
            card_id = int(match["id"])
            winners = set(match["winners"].split())
            numbers = set(match["numbers"].split())
            assert card_id not in cards
            cards[card_id] = (winners, numbers)
    return cards


def get_number_of_winning_numbers(winners, numbers):
    return len(winners.intersection(numbers))


def main():
    cards = parse("input.txt")
    part_one(cards.copy())
    part_two(cards.copy())


if __name__ == "__main__":
    main()

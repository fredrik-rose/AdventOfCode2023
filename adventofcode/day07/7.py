# Day 7: Camel Cards
import dataclasses
import collections as coll


@dataclasses.dataclass
class Hand:
    cards: list
    bet: int


def part_one(hands):
    answer = play_game(hands, get_rank)
    print(f"Part one: {answer}")


def part_two(hands):
    answer = play_game(hands, joker=11)
    print(f"Part two: {answer}")


def parse(file_path):
    hands = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            cards, bet = line.split()
            cards = [convert_card_to_number(e) for e in cards]
            bet = int(bet)
            hands.append(Hand(cards, bet))
    return hands


def convert_card_to_number(card):
    return {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }[card]


def play_game(hands, joker=None):
    hands = sorted(hands, key=lambda x: get_rank(x.cards, joker))
    money = sum(e.bet * (i + 1) for i, e in enumerate(hands))
    return money


def get_rank(cards, joker):
    counter = coll.Counter(cards)
    jokers = counter[joker]
    del counter[joker]
    if counter:
        first = sorted(counter.values(), reverse=True)
        first[0] += jokers
    else:
        first = [len(cards)]
    second = [1 if e == joker else e for e in cards]
    return (first, second)


def main():
    hands = parse("input.txt")
    part_one(hands.copy())
    part_two(hands.copy())


if __name__ == "__main__":
    main()

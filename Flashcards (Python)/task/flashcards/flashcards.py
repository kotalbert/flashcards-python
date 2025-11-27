"""Flashcards application module."""

from dataclasses import dataclass


@dataclass
class Flashcard:
    term: str
    definition: str


def main():
    cards = []
    print("Input the number of cards:")
    n_cards = int(input())

    for i in range(1, n_cards + 1):
        print(f"The term for card #{i}:")
        term = input()
        print(f"The definition for card #{i}:")
        definition = input()
        cards.append(Flashcard(term, definition))

    for c in cards:
        term = c.term
        definition = c.definition
        print(f'Print the definition of "{term}":')
        answer = input()

        if answer == definition:
            print("Correct!")
        else:
            print(f"Wrong. The right answer is \"{definition}\".")


if __name__ == "__main__":
    main()

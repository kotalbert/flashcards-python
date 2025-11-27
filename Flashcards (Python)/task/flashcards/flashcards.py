"""Flashcards application module."""

from dataclasses import dataclass


@dataclass
class Flashcard:
    term: str
    definition: str


def main():
    cards = {}
    print("Input the number of cards:")
    n_cards = int(input())

    for i in range(1, n_cards + 1):
        print(f"The term for card #{i}:")
        # guard against duplicate terms
        while True:
            term = input()
            if term in cards:
                print(f'The term "{term}" already exists. Try again:')
            else:
                break

        print(f"The definition for card #{i}:")
        while True:
            # check if term or definition already exists
            definition = input()
            if any(c.definition == definition for c in cards.values()):
                print(f'The definition "{definition}" already exists. Try again:')
            else:
                break

        cards[term] = Flashcard(term, definition)

    for term, c in cards.items():
        definition = c.definition
        print(f'Print the definition of "{term}":')
        answer = input()

        if answer == definition:
            print("Correct!")
        else:
            matched = False
            for other_term, other_card in cards.items():
                if other_card.definition == answer:
                    print(
                        f'Wrong. The right answer is "{definition}", but your definition is correct for "{other_term}".')
                    matched = True
                    break
            if not matched:
                print(f'Wrong. The right answer is "{definition}".')


if __name__ == "__main__":
    main()

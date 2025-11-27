"""Flashcards application module."""

from dataclasses import dataclass
from random import choice


@dataclass
class Flashcard:
    term: str
    definition: str


class Deck:
    """Class representing a deck of flashcards."""

    def __init__(self):
        self.cards = {}

    def add_card(self, term: str, definition: str):
        """Add a new flashcard to the deck.

        Guard against duplicate terms and definitions.
        Raises ValueError if term or definition already exists.
        """

        if term in self.cards:
            raise ValueError(f'The term "{term}" already exists.')
        if any(c.definition == definition for c in self.cards.values()):
            raise ValueError(f'The definition "{definition}" already exists.')
        self.cards[term] = Flashcard(term, definition)

    def remove_card(self, term: str):
        """Remove a flashcard from the deck by its term."""

        if term in self.cards:
            del self.cards[term]
        else:
            raise ValueError(f'Can\'t remove "{term}": there is no such card.')

    def update_card(self, term: str, new_definition: str):
        """Update the definition of an existing flashcard."""

        if term not in self.cards:
            raise ValueError(f'Can\'t update "{term}": there is no such card.')
        if any(c.definition == new_definition for c in self.cards.values()):
            raise ValueError(f'The definition "{new_definition}" already exists.')
        self.cards[term].definition = new_definition


def main():
    deck = Deck()
    while True:
        display_menu(deck)


def handle_remove_command(deck):
    try:
        print("Which card?")
        term = input()
        deck.remove_card(term)
        print("The card has been removed.")
    except ValueError as e:
        print(e)


def handle_import_command(deck):
    print("File name:")
    filename = input()
    try:
        with open(filename, "r") as file:
            n_imported = 0
            for line in file:
                term, definition = line.strip().split(":")
                try:
                    deck.add_card(term, definition)
                    n_imported += 1
                except ValueError:
                    # update existing card
                    deck.update_card(term, definition)
            print(f"{n_imported} cards have been loaded.")
    except FileNotFoundError:
        print("File not found.")


def handle_export_command(deck):
    print("File name:")
    filename = input()
    with open(filename, "w") as file:
        for card in deck.cards.values():
            file.write(f"{card.term}: {card.definition}\n")
    print(f"{len(deck.cards)} cards have been saved.")


def handle_ask_command(deck):
    print("How many times to ask?")
    n_ask = int(input())
    terms = list(deck.cards.keys())
    for _ in range(n_ask):
        term = choice(terms)
        card = deck.cards[term]
        print(f'Print the definition of "{term}":')
        answer = input()
        if answer == card.definition:
            print("Correct!")
        else:
            matched = False
            for other_term, other_card in deck.cards.items():
                if other_card.definition == answer:
                    print(
                        f'Wrong. The right answer is "{card.definition}", but your definition is correct for "{other_term}".')
                    matched = True
                    break
            if not matched:
                print(f'Wrong. The right answer is "{card.definition}".')


def display_menu(deck: Deck):
    print("Input the action (add, remove, import, export, ask, exit):")
    command = input()
    match command.lower():
        case "add":
            handle_add_command(deck)
        case "remove":
            handle_remove_command(deck)
        case "import":
            handle_import_command(deck)
        case "export":
            handle_export_command(deck)
        case "ask":
            handle_ask_command(deck)
        case "exit":
            print("Bye bye!")
            exit(0)
        case _:
            print(f'Unknown command: "{command}"')


def handle_add_command(deck: Deck):
    try:
        print("The term for the new card:")
        term = input()
        print("The definition for the new card:")
        definition = input()
        deck.add_card(term, definition)
        print(f'The pair ("{term}":"{definition}") has been added.')
    except ValueError as e:
        print(e)


def add_cards():
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

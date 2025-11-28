"""Flashcards application module."""

import io
from dataclasses import dataclass
from random import choice


@dataclass
class Flashcard:
    term: str
    definition: str
    number_tried: int = 0


class Deck:
    """Class representing a deck of flashcards."""

    def __init__(self):
        self.cards = {}

    def add_card(self, term: str, definition: str, number_tried: int = 0):
        """Add a new flashcard to the deck.

        Guard against duplicate terms and definitions.
        Raises ValueError if term or definition already exists.
        """

        if term in self.cards:
            raise ValueError(f'The term "{term}" already exists.')
        if any(c.definition == definition for c in self.cards.values()):
            raise ValueError(f'The definition "{definition}" already exists.')
        self.cards[term] = Flashcard(term, definition, number_tried)

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
        # if any(c.definition == new_definition for c in self.cards.values()):
        #     raise ValueError(f'The definition "{new_definition}" already exists.')
        self.cards[term].definition = new_definition

    def get_hardest_cards(self) -> list[Flashcard]:
        """Return a list of the hardest cards based on number of incorrect tries."""

        if not self.cards:
            return []

        max_tries = max(card.number_tried for card in self.cards.values())
        if max_tries == 0:
            return []

        hardest_cards = [card for card in self.cards.values() if card.number_tried == max_tries]
        return hardest_cards

    def reset_cards_stats(self):
        """Reset the number of incorrect tries for all cards."""

        for card in self.cards.values():
            card.number_tried = 0

def main():
    deck = Deck()
    log = io.StringIO()
    while True:
        display_menu(deck, log)


def handle_remove_command(deck: Deck, log: io.StringIO):
    try:
        card_ = "Which card?"
        print(card_)
        log.write(card_ + "\n")
        term = input()
        deck.remove_card(term)
        removed_ = "The card has been removed."
        print(removed_)
        log.write(removed_ + "\n")
    except ValueError as e:
        print(e)
        log.write(str(e))


def handle_import_command(deck: Deck, log: io.StringIO):
    name_ = "File name:"
    print(name_)
    log.write(name_ + "\n")
    filename = input()
    try:
        with open(filename, "r") as file:
            n_imported = 0
            for line in file:
                term, definition, number_tried = line.strip().split(":")
                try:
                    deck.add_card(term, definition, int(number_tried))
                    n_imported += 1
                except ValueError:
                    # update existing card
                    deck.update_card(term, definition)
                    n_imported += 1  # updating also counts as importing
            loaded_ = f"{n_imported} cards have been loaded."
            print(loaded_)
            log.write(loaded_ + "\n")
    except FileNotFoundError:
        found_ = "File not found."
        print(found_)
        log.write(found_ + "\n")


def handle_export_command(deck: Deck, log: io.StringIO):
    name_ = "File name:"
    print(name_)
    log.write(name_ + "\n")
    filename = input()
    with open(filename, "w") as file:
        for card in deck.cards.values():
            file.write(f"{card.term}:{card.definition}:{card.number_tried}\n")
    saved_ = f"{len(deck.cards)} cards have been saved."
    print(saved_)
    log.write(saved_ + "\n")


def handle_ask_command(deck: Deck, log: io.StringIO):
    ask_ = "How many times to ask?"
    print(ask_)
    log.write(ask_ + "\n")
    n_ask = int(input())
    terms = list(deck.cards.keys())
    for _ in range(n_ask):
        term = choice(terms)
        card = deck.cards[term]
        term_ = f'Print the definition of "{term}":'
        print(term_)
        log.write(term_ + "\n")
        answer = input()
        if answer == card.definition:
            correct_ = "Correct!"
            print(correct_)
            log.write(correct_ + "\n")
        else:
            matched = False
            for other_term, other_card in deck.cards.items():
                if other_card.definition == answer:
                    term__ = f'Wrong. The right answer is "{card.definition}", but your definition is correct for "{other_term}".'
                    card.number_tried += 1
                    print(term__)
                    log.write(term__ + "\n")
                    matched = True
                    break
            if not matched:
                definition__ = f'Wrong. The right answer is "{card.definition}".'
                card.number_tried += 1
                print(definition__)
                log.write(definition__ + "\n")


def handle_log_command(deck: Deck, log: io.StringIO):
    filename_ = "File name:"
    print(filename_)
    log.write(filename_ + "\n")
    filename = input()
    log.write(filename + "\n")
    with open(filename, "w") as file:
        file.write(log.getvalue())
    saved_ = "The log has been saved."
    print(saved_)
    log.write(saved_ + "\n")


def handle_hardest_card_command(deck: Deck, log: io.StringIO):
    hardest_cards = deck.get_hardest_cards()
    if len(hardest_cards) == 0:
        no_cards_ = "There are no cards with errors."
        print(no_cards_)
        log.write(no_cards_ + "\n")
    elif len(hardest_cards) == 1:
        card = hardest_cards[0]
        one_card_ = f'The hardest card is "{card.term}". You have {card.number_tried} errors answering it.'
        print(one_card_)
        log.write(one_card_ + "\n")
    else:
        terms = '", "'.join(card.term for card in hardest_cards)
        n_errors = hardest_cards[0].number_tried
        multiple_cards_ = f'The hardest cards are "{terms}". You have {n_errors} errors answering them.'
        print(multiple_cards_)
        log.write(multiple_cards_ + "\n")


def handle_reset_stats_command(deck: Deck, log: io.StringIO):
    deck.reset_cards_stats()
    reset_ = "Card statistics have been reset."
    print(reset_)
    log.write(reset_ + "\n")


def display_menu(deck: Deck, log: io.StringIO):
    stats_ = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
    print(stats_)
    log.write(stats_ + "\n")
    command = input()
    log.write(command + "\n")
    match command.lower():
        case "add":
            handle_add_command(deck, log)
        case "remove":
            handle_remove_command(deck, log)
        case "import":
            handle_import_command(deck, log)
        case "export":
            handle_export_command(deck, log)
        case "ask":
            handle_ask_command(deck, log)
        case "exit":
            print("Bye bye!")
            exit(0)
        case "log":
            handle_log_command(deck, log)
        case "hardest card":
            handle_hardest_card_command(deck, log)
        case "reset stats":
            handle_reset_stats_command(deck, log)
        case _:
            print(f'Unknown command: "{command}"')


def handle_add_command(deck: Deck, log: io.StringIO):
    try:
        card_ = "The term for the new card:"
        print(card_)
        log.write(card_ + "\n")
        while True:
            term = input()
            log.write(term + "\n")
            if term in deck.cards:
                again_ = f'The term "{term}" already exists. Try again:'
                print(again_)
                log.write(again_ + "\n")
            else:
                break
        new_card_ = "The definition for the new card:"
        print(new_card_)
        log.write(new_card_ + "\n")
        while True:
            definition = input()
            if any(c.definition == definition for c in deck.cards.values()):
                try_again_ = f'The definition "{definition}" already exists. Try again:'
                print(try_again_)
                log.write(try_again_ + "\n")
            else:
                break
        deck.add_card(term, definition)
        added_ = f'The pair ("{term}":"{definition}") has been added.'
        print(added_)
        log.write(added_ + "\n")
    except ValueError as e:
        print(e)
        log.write(str(e) + "\n")


def add_cards(log: io.StringIO):
    cards = {}
    cards_ = "Input the number of cards:"
    print(cards_)
    log.write(cards_ + "\n")
    n_cards = int(input())
    log.write(cards_ + "\n")

    for i in range(1, n_cards + 1):
        i_ = f"The term for card #{i}:"
        print(i_)
        log.write(i_ + "\n")

        # guard against duplicate terms
        while True:
            term = input()
            if term in cards:
                again_ = f'The term "{term}" already exists. Try again:'
                print(again_)
                log.write(again_ + "\n")
            else:
                break

        card_i_ = f"The definition for card #{i}:"
        print(card_i_)
        log.write(card_i_ + "\n")
        while True:
            # check if term or definition already exists
            definition = input()
            if any(c.definition == definition for c in cards.values()):
                try_again_ = f'The definition "{definition}" already exists. Try again:'
                print(try_again_)
                log.write(try_again_ + "\n")
            else:
                break

        cards[term] = Flashcard(term, definition)

    for term, c in cards.items():
        definition = c.definition
        term_ = f'Print the definition of "{term}":'
        print(term_)
        log.write(term_ + "\n")

        answer = input()
        log.write(answer + "\n")

        if answer == definition:
            correct_ = "Correct!"
            print(correct_)
            log.write(correct_ + "\n")

        else:
            matched = False
            for other_term, other_card in cards.items():
                if other_card.definition == answer:
                    term__ = f'Wrong. The right answer is "{definition}", but your definition is correct for "{other_term}".'
                    print(term__)
                    log.write(term__ + "\n")
                    matched = True
                    break
            if not matched:
                definition__ = f'Wrong. The right answer is "{definition}".'
                print(definition__)
                log.write(definition__ + "\n")


if __name__ == "__main__":
    main()

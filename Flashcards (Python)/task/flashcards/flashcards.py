"""Flashcards application module."""


def main():
    term = input()
    definition = input()
    answer = input()

    if answer == definition:
        print("Your answer is right!")
    else:
        print("Your answer is wrong...")


if __name__ == "__main__":
    main()

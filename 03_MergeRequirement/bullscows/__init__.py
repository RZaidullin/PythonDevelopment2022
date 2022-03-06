import textdistance as td
import random


def bullscows(guess: str, secret_word:str) -> (int, int):
    bulls = td.hamming.similarity(guess, secret_word)
    cows = td.sorensen_dice(guess, secret_word)*len(guess) - bulls
    return (bulls, cows)


def ask(hint: str, words: list[str] = None) -> str:
    guess = input(hint)
    if words:
        while guess not in words:
            print("Your guess is not from the dictionary")
            guess = input(hint)
    return guess


def inform(fmt: str, bulls: int, cows: int) -> None:
    print(fmt.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> str:
    secret = random.choice(words)
    guesses = 0
    while True:
        guess = ask("Enter your guess: ", words)
        guesses += 1
        res = bullscows(guess, secret)
        inform("Bulls: {}, Cows: {}", *res)
        if res[0] == len(secret):
            return guesses

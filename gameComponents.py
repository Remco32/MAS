# Good resource for the game: https://www.ultraboardgames.com/hanabi/game-rules.php
# The 60 cards. 5 colours + 1 rainbow set, with 10 cards each.
# values of the cards 1, 1, 1, 2, 2, 3, 3, 4, 4, 5

import random
import gameSettings
from colorama import Fore, Style


class Card:
    def __init__(self, colour, value, ID=-1):
        self.colour = colour  # {red, yellow, green, blue, white} or 'rainbow'
        self.value = value  # 1 to 5
        self.cardID = ID  # unique ID for card, to avoid duplicates (e.g. red 1 and red 1)

    def print_card(self):
        # Changing print colours
        if self.colour == 'red':
            print(Fore.RED, end='')
        if self.colour == 'yellow':
            print(Fore.YELLOW, end='')
        if self.colour == 'green':
            print(Fore.GREEN, end='')
        if self.colour == 'blue':
            print(Fore.BLUE, end='')
        if self.colour == 'rainbow':
            print(Fore.LIGHTBLACK_EX, end='')
        print(str(self.colour) + " " + str(self.value), end='')
        print(Style.RESET_ALL, end='')


# Contains all the cards at the start of the game. Re
class Deck:
    def __init__(self):

        self.colours_in_game = ['red', 'yellow', 'green', 'blue', 'white']
        self.colours_in_game = self.colours_in_game[0:gameSettings.suit_amount]

        if gameSettings.use_rainbow_card:
            self.colours_in_game = self.colours_in_game[0:gameSettings.suit_amount-1]
            self.colours_in_game.append('rainbow')
        if gameSettings.use_single_cards:
            self.values_in_game = [1, 2, 3, 4, 5]
        else:
            self.values_in_game = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        self.deck_contents = []
        self.generate_deck()

        # Set IDs
        for i in range(len(self.deck_contents)):
            self.deck_contents[i].cardID = i

    # For drawing a card from the deck. Randomized, so no need to shuffle the deck.
    def get_new_card(self):
        # Check if there are still cards in the deck
        if self.deck_contents:
            # Remove a card from the deck at a random location, and returns is
            return self.deck_contents.pop(random.randint(0, len(self.deck_contents) - 1))
        else:
            return None

    def generate_deck(self):
        # Generate deck
        self.deck_contents = [Card(c, v) for c in self.colours_in_game for v in self.values_in_game]

    def print_colours_in_game(self):
        print("(", end='')
        for colour in self.colours_in_game:

            if not self.colours_in_game[-1] == colour:
                print(colour, end=", ")
                if colour is 'rainbow':
                    print(")")
                else:
                    print(colour + ")")




class Discard:
    def __init__(self):
        self.discard_pile = []

    def add_to_discard(self, card):
        self.discard_pile.append(card)


class Tokens:
    def __init__(self):
        # Note tokens are used to ask for a hint
        self.max_note_tokens = 8
        self.note_tokens = self.max_note_tokens

        # Storm tokens are basically lives. Run out and the game ends.
        self.storm_tokens = 3

    def decrease_storm_tokens(self):
        self.storm_tokens -= 1
        print(Fore.RED, "Storm token deducted")
        print(Style.RESET_ALL)
        self.print_tokens()

    def increase_note_tokens(self):
        if self.note_tokens < self.max_note_tokens:
            self.note_tokens += 1
            print("Note token earned. ", end='')
            self.print_tokens()

    def decrease_note_tokens(self):
        self.note_tokens -= 1
        print("Note token used. ", end='')
        self.print_tokens()

    def print_tokens(self):
        print("Note tokens left: " + str(self.note_tokens) + "/" + str(self.max_note_tokens) + ". Storm tokens left: " + str(self.storm_tokens) + "/3.")

# Good resource for the game: https://www.ultraboardgames.com/hanabi/game-rules.php
# The 60 cards. 5 colours + 1 rainbow set, with 10 cards each.
# values of the cards 1, 1, 1, 2, 2, 3, 3, 4, 4, 5

# # # # #
# Settings
# # # # #
use_rainbow_card = False


import random

class Card:
    def __init__(self, colour, value, ID=-1):
        self.colour = colour    # {red, yellow, green, blue, white} or 'rainbow'
        self.value = value      # 1 to 5
        self.cardID = ID        # unique ID for card, to avoid duplicates (e.g. red 1 and red 1)


# Contains all the cards at the start of the game. Re
class Deck:
    def __init__(self):

        colours = ['red', 'yellow', 'green', 'blue', 'white']
        if use_rainbow_card:
            colours.append('rainbow')
        values = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

        # Generate deck
        self.deck_contents = [Card(c,v) for c in colours for v in values]

        # Set IDs
        for i in range(len(self.deck_contents)):
            self.deck_contents[i].cardID = i

    # For drawing a card from the deck. Randomized, so no need to shuffle the deck.
    def get_new_card(self):
        # Remove a card from the deck at a random location, and returns is
        return self.deck_contents.pop(random.randint(0, len(self.deck_contents)-1))


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

        self.storm_tokens = 3

"""
# Contains the deck, discard, tokens
class Table:
    # Set up the table with a deck, an empty discard pile and the tokens
    def __init__(self):
"""

deck = Deck()
discard = Discard()
discard.add_to_discard(deck.get_new_card())


print()

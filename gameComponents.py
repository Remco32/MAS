# The 60 cards. 5 colours + 1 rainbow set, with 10 cards each.
# values of the cards 1, 1, 1, 2, 2, 3, 3, 4, 4, 5

class Card:
    def __init__(self, colour, value, ID=-1):
        self.colour = colour    # {red, yellow, green, blue, white} or 'rainbow'
        self.value = value      # 1 to 5
        self.cardID = ID        # unique ID for card, to avoid duplicates (e.g. red 1 and red 1)

        def set_card_id(ID):
            self.cardID = ID

# Contains all the cards at the start of the game. Re
class Deck:
    def __init__(self):
        colours = ('red', 'yellow', 'green', 'blue', 'white', 'rainbow')
        values = (1, 1, 1, 2, 2, 3, 3, 4, 4, 5)

        # Generate deck
        self.deck_contents = [Card(c,v) for c in colours for v in values]

        # Set IDs
        for i in range(len(self.deck_contents)):
            self.deck_contents[i].cardID = i

    # For drawing a card from the deck
    #def get_new_card:


# class Discard:

# Contains the deck, discard, tokens
# class Table:

deck = Deck()
print()

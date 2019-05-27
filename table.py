import gameComponents

# Contains the deck, discard, tokens
class Table:
    # Set up the table with a deck, an empty discard pile and the tokens
    def __init__(self):
        self.deck = gameComponents.Deck()
        self.discard = gameComponents.Discard()
        self.tokens = gameComponents.Tokens()
import gameComponents
import gameSettings
import player

# Contains the deck, discard, tokens
class Table:
    # Set up the table with a deck, an empty discard pile and the tokens
    def __init__(self):
        self.deck = gameComponents.Deck()
        self.discard = gameComponents.Discard()
        self.tokens = gameComponents.Tokens()

        self.player_list = []
        for i in range(gameSettings.player_amount):
            new_player = player.Player(self.deck)
            self.player_list.append(new_player)
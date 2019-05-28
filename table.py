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
        self.play_area = [[] for i in range(5)] # Create 5 empty piles for playing the cards

        self.player_list = []
        for i in range(gameSettings.player_amount):
            new_player = player.Player(self.deck)
            self.player_list.append(new_player)

    def print_piles(self):
        i = 0
        for pile in range(len(self.play_area)):
            print("Pile " + str(i) + ": ", end='')
            for card in self.play_area[pile]:
                print(str(card.colour) + " " + str(card.value), end='; ')
            print()
            i = i + 1


    # To place a card on one of the piles in the play area
    def place_card(self, card, pile_number):
        if pile_number > 4: # There are only 5 piles
            raise Exception("Illegal move: pile " + str(pile_number) + " doesn't exist.")
        if len(self.play_area[pile_number]) + 1 != card.value:
            raise Exception("Illegal move: can't place value " + str(card.value) +
                            " on index " + str(len(self.play_area[pile_number])) + " of the pile.")
        self.play_area[pile_number].append(card)


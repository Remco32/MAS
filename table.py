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
            new_player = player.Player(self.deck, i)
            self.player_list.append(new_player)

        self.total_turn_counter = 0
        self.current_player = self.player_list[self.total_turn_counter]

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
            print("Can't place value " + str(card.value) +
                            " on index " + str(len(self.play_area[pile_number])) + " of the pile.")
            self.tokens.storm_tokens -= 1
            print("Storm token deducted")
            self.tokens.print_tokens()
            return
        if len(self.play_area[pile_number]) > 0:
            if self.play_area[pile_number][0].colour != card.colour:
                print("Wrong colour placed on this pile.")
                self.tokens.storm_tokens -= 1
                print("Storm token deducted")
                self.tokens.print_tokens()
                return
        self.play_area[pile_number].append(card)
        # Bonus scoring
        if self.play_area[pile_number] == 5:
            self.tokens.increase_note_tokens()

    # Returns 0 for none, 1 for win, 2 for final round, -1 for loss.
    def check_end_conditions(self):
        # All storm tokens flipped
        if self.tokens.storm_tokens <= 0:
            return -1
        # All piles filled correctly
        if self.count_points() == 25:
            return 1
        if len(self.deck.deck_contents) == 0:
            return 2

    def pass_turn(self):
        self.total_turn_counter += 1
        next_player = self.total_turn_counter % 3
        self.current_player = self.player_list[next_player]

    def count_points(self):
        points = 0
        for pile in range(len(self.play_area)):
            points += len(self.play_area[pile])
        return points




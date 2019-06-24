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
        self.play_area = [[] for i in range(gameSettings.suit_amount)] # Create 5 empty piles for playing the cards

        self.player_list = []
        for i in range(gameSettings.player_amount):
            new_player = player.Player(self.deck, i, self)
            self.player_list.append(new_player)

        # Update representation after dealing cards
        for player_loop in self.player_list:
            for card in player_loop.hand:
                self.update_cards_left_representation_other_players(card, player_loop)

        self.total_turn_counter = 0
        self.current_player = self.player_list[self.total_turn_counter]

    def print_piles(self):
        i = 0
        print("Current piles:")
        for pile in range(len(self.play_area)):
            print("Pile " + str(i) + ": ", end='')
            for card in self.play_area[pile]:
                print(str(card.colour) + " " + str(card.value), end='; ')
            print()
            i = i + 1
        print()

    def print_other_players_hands(self):
        print("Available players (with their hands):")
        for player in self.player_list:
            if player is not self.current_player:
                player.print_hand(player.playerID)
        print()

    def print_game_status(self):
        print("[Game state]:")
        if not gameSettings.CHEAT_show_own_hand:
            self.print_other_players_hands()
        else:
            for player in self.player_list:
                player.print_hand(player.playerID)
        self.print_piles()
        self.tokens.print_tokens()
        print()


    # To place a card on one of the piles in the play area
    def place_card(self, card):

        # Cases where you can't play
        #if pile_number > len(self.deck.colours_in_game):
        #    raise Exception("Illegal move: pile " + str(pile_number) + " doesn't exist.")

        # Select correct pile
        pile_number = self.deck.colours_in_game.index(card.colour)

        if len(self.play_area[pile_number]) + 1 != card.value:
            print("Can't place value " + str(card.value) +
                            " on index " + str(len(self.play_area[pile_number])) + " of the pile.")
            self.tokens.decrease_storm_tokens()
            return
        if len(self.play_area[pile_number]) > 0:
            if self.play_area[pile_number][0].colour != card.colour:
                print("Wrong colour placed on this pile.")
                self.tokens.decrease_storm_tokens()
                return

        # Case where you can play
        self.play_area[pile_number].append(card)
        self.current_player.update_cards_left_representation(self, card)

        # Bonus scoring
        if self.play_area[pile_number] == max(self.deck.values_in_game)-1:
            print("Pile completely filled!")
            self.tokens.increase_note_tokens()

    # Returns 0 for none, 1 for win, 2 for final round, -1 for loss.
    def check_end_conditions(self):
        # All storm tokens flipped
        if self.tokens.storm_tokens <= 0:
            return -1
        # All piles filled correctly
        if self.count_points() == max(self.deck.values_in_game) * len(self.deck.colours_in_game):
            return 1
        if len(self.deck.deck_contents) == 0:
            return 2

    # Returns a list of all cards that are currently playable
    def get_playable_cards(self):
        playable_cards = []
        for i in range(len(self.play_area)):
            if len(self.play_area[i]) > 0:
                if len(self.play_area[i]) != 5:
                    playable_cards.append([self.play_area[i][-1].colour, len(self.play_area[i]) + 1])
            else:
                playable_cards.append([self.deck.colours_in_game[i], 1])
        return playable_cards

    def pass_turn(self):
        self.total_turn_counter += 1
        next_player = self.total_turn_counter % gameSettings.player_amount
        self.current_player = self.player_list[next_player]

    def count_points(self):
        points = 0
        for pile in range(len(self.play_area)):
            points += len(self.play_area[pile])
        return points

    def update_cards_left_representation_other_players(self, card, ignored_player):
        for player_local in self.player_list:
            if player_local is not ignored_player:
                player_local.update_cards_left_representation(self, card)
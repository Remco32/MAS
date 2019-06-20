import gameSettings

class Player:
    def __init__(self, deck, playerID, table):
        self.hand = []
        self.playerID = playerID

        for i in range(gameSettings.hand_size):
            self.hand.append(deck.get_new_card())

        # Generate internal representation of the cards that are still in the game (i.e. not visible for the player)
        self.cards_left_representation = self.generate_cards_left_representation(deck, table)

    def print_cards_left_representation(self, deck):
        i = 0
        print("Values: ", end='')
        print(*range(1, max(deck.values_in_game) + 1))
        for colour in deck.colours_in_game:
            print(str(colour) + ": " + str(self.cards_left_representation[i]))
            i += 1
        print()

    def generate_cards_left_representation(self, deck, table):
        # Generate data structure
        representation = []
        for colour in deck.colours_in_game:
            sublist = []
            for value in range(1, max(deck.values_in_game)+1):
                sublist.append(deck.values_in_game.count(value))
            representation.append(sublist)
        return representation

    def update_cards_left_representation(self, table, card):
        # Get index of colour of card that has been played
        index = table.deck.colours_in_game.index(card.colour)

        # Update for value of the card
        self.cards_left_representation[index][card.value-1] -= 1


    def print_hand(self, playerID=None):
        i = 0
        if playerID is not None:
            print("Player " + str(playerID), end=": ")
        for card in self.hand:
            print("Card " + str(i) + ": " + str(card.colour) + " " + str(card.value), end=" | ")
            i = i + 1
        print()


    def HUMAN_player_selector(self, table):
        #print("Available players:")
        for player in table.player_list:
            if player is not self:
            #print("Player " + str(player.playerID) + ": " + str(player.print_hand()))
                player.print_hand(player.playerID)
        input_player = int(input("Which player to pick?"))
        if table.player_list[input_player] is self:
            print("You can't pick yourself.")
            self.HUMAN_player_selector(table)
        else:
            return table.player_list[input_player]

    def HUMAN_colour_selector(self, table):
        print("Pick a colour: ", end='')
        #for colour in table.deck.colours_in_game:
        #    print(colour, end=' ')
        selected_colour = str(input())
        if selected_colour not in table.deck.colours_in_game:
            print("Invalid colour, try again...")
            self.HUMAN_colour_selector(table)
        else:
            return str(selected_colour)

    def HUMAN_value_selector(self, table):
        print("Pick a value (1-5): ", end='')

        selected_value = int(input())
        if not (5 >= int(selected_value) > 0):
            print("Invalid value, try again...")
            self.HUMAN_value_selector(table)
        else:
            return selected_value


    def HUMAN_play_card(self, table):
        if gameSettings.show_own_hand:
            print("Current player has these cards:")
            self.print_hand()
        print("Current player has " + str(len(self.hand)) + " cards")
        input_card = int(input("Which card to play? (0-" + str(len(self.hand)-1) + ")"))
        table.print_piles()
        input_pile = int(input("Which pile to play to?"))
        self.play_card(self.hand[input_card], table, input_pile)

    def play_card(self, card, table, pile_number):
        table.place_card(card, pile_number)
        #self.update_cards_left_representation(table, card) # Done in table.py
        index_card = self.hand.index(card)
        self.hand[index_card] = None
        # Take new card, if possible
        new_card = table.deck.get_new_card()
        if new_card is not None:
            self.hand[index_card] = new_card
            table.update_cards_left_representation_other_players(new_card, self)

    def HUMAN_discard_card(self, table):
        if gameSettings.show_own_hand:
            print("Current player has these cards:")
            self.print_hand()
        print("Current player has " + str(len(self.hand)) + " cards")
        input_card = int(input("Which card to discard? (0-" + str(len(self.hand)-1) + ")"))
        input_card = self.hand[input_card]
        self.discard_card(input_card, table)

    def discard_card(self, card, table):
        table.discard.add_to_discard(card)
        self.update_cards_left_representation(table, card)
        index_card = self.hand.index(card)
        self.hand[index_card] = None
        # Regain a note, if possible token for discarding
        table.tokens.increase_note_tokens()
        # Take new card, if possible
        new_card = table.deck.get_new_card()
        if new_card is not None:
            self.hand[index_card] = new_card
            table.update_cards_left_representation_other_players(new_card, self)

    def HUMAN_give_colour_hint(self, table):
        selected_player = self.HUMAN_player_selector(table)
        selected_colour = self.HUMAN_colour_selector(table)
        self.give_colour_hint(selected_player, selected_colour, table)


    def give_colour_hint(self, player, colour, table):
        cards_indices = []
        index = 0
        for card in player.hand:
            if card.colour == colour or card.colour == 'rainbow':
                cards_indices.append(index)
            index += 1
        # For now, hints are just 'announced' as prints
        print("Player " + str(player.playerID) + ", you have the colour " + str(colour), end="")
        if not cards_indices:
            print(" nowhere.")
        else:
            print(" at card indices " + str(cards_indices))
        table.tokens.decrease_note_tokens()

    def HUMAN_give_value_hint(self, table):
        selected_player = self.HUMAN_player_selector(table)
        selected_value = self.HUMAN_value_selector(table)
        self.give_value_hint(selected_player, selected_value, table)

    def give_value_hint(self, player, value, table):
        cards_indices = []
        index = 0
        for card in player.hand:
            if card.value == value:
                cards_indices.append(index)
            index += 1
        # For now, hints are just 'announced' as prints
        print("Player " + str(player.playerID) + ", you have the value " + str(value), end="")
        if not cards_indices:
            print(" nowhere.")
        else:
            print(" at card indices " + str(cards_indices))
        table.tokens.decrease_note_tokens()

    def HUMAN_pick_action(self, table):
        print("Player " + str(self.playerID) + ", pick an action:")
        input_action = int(
            input("Give a colour hint (0), give a value hint (1), discard a card (2) or play a card (3)"))

        # Why are there no switch statements, Python..?

        if input_action is 0 and table.tokens.note_tokens > 0:
            self.HUMAN_give_colour_hint(table)
        elif input_action is 1 and table.tokens.note_tokens > 0:
            self.HUMAN_give_value_hint(table)
        elif input_action is 2:
            self.HUMAN_discard_card(table)
        elif input_action is 3:
            self.HUMAN_play_card(table)
        else:
            print("Invalid input or illegal move, try again...")
            self.HUMAN_pick_action(table)

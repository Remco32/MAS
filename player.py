import gameSettings


class Player:
    def __init__(self, deck, playerID, table):
        self.hand = []
        self.playerID = playerID

        for i in range(gameSettings.hand_size):
            self.hand.append(deck.get_new_card())

        # Generate internal representation of the cards that are still in the game (i.e. not visible for the player)
        self.cards_left_representation = self.generate_cards_left_representation(deck, table)
        self.hand_knowledge = [None] * gameSettings.hand_size
        self.generate_hand_knowledge()

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
            for value in range(1, max(deck.values_in_game) + 1):
                sublist.append(deck.values_in_game.count(value))
            representation.append(sublist)
        return representation

    def generate_hand_knowledge(self):
        for i in range(0, gameSettings.hand_size):
            self.update_card_knowledge(i)

    def update_cards_left_representation(self, table, card):
        # Get index of colour of card that has been played
        index = table.deck.colours_in_game.index(card.colour)

        # Update for value of the card
        self.cards_left_representation[index][card.value - 1] -= 1
        self.update_hand_knowledge()

    # Update the knowledge about a certain card at a given index, used to reset knowledge after a new card is drawn
    def update_card_knowledge(self, index):
        rep_copy = []
        for i in range(len(self.cards_left_representation)):
            sublist = []
            for j in range(len(self.cards_left_representation[i])):
                value = self.cards_left_representation[i][j]
                if value == 0:
                    sublist.append(0)
                else:
                    sublist.append(1)
            rep_copy.append(sublist)
        self.hand_knowledge[index] = rep_copy

    # Update the knowledge of the whole hand while keeping current knowledge in mind, used after another player draws a new card
    # Needed so as to not overwrite earlier gained hints
    def update_hand_knowledge(self):
        for card_index in range(len(self.hand_knowledge)):
            for colour in range(len(self.cards_left_representation)):
                for rank in range(len(self.cards_left_representation[colour])):
                    self.hand_knowledge[card_index][colour][rank] *= self.cards_left_representation[colour][rank]

    def print_hand(self, playerID=None):
        i = 0
        if playerID is not None:
            print("Player " + str(playerID), end=": ")
        for card in self.hand:
            print("Card " + str(i) + ": " + str(card.colour) + " " + str(card.value), end=" | ")
            i = i + 1
        print()

    ## CHECKS ##

    # Check if the player knows what the card at a given hand index is, and if so, return the colour and rank of that card
    def knows_card(self, table, index):
        card = self.hand_knowledge[index]
        colour = 0
        rank = 0
        result = 0
        for i in range(len(card)):
            for j in range(len(card[i])):
                if card[i][j]:
                    colour = i
                    rank = j + 1
                    result += 1
                    if result > 1:
                        return None
        return table.deck.colours_in_game[colour], rank

    ## PASSIVE GAME ACTIONS ##

    def announce_colour(self, cards_indices, colour, table):
        announced_colour_index = table.deck.colours_in_game.index(colour)
        for card_index in range(len(self.hand_knowledge)):
            card = self.hand_knowledge[card_index]
            if cards_indices is not None and card_index in cards_indices:
                # Card with this index is colour or rainbow
                for colour_index in range(len(card) - 1):  # Rainbow is always the final index, no need to change knowledge there
                    # Set all colours other than the announced one to false
                    if colour_index != announced_colour_index:
                        for i in range(len(card[colour_index])):
                            card[colour_index][i] *= 0
            else:
                # Card with this index is not colour or rainbow
                for colour_index in range(
                        len(card)):  # This time include rainbow, because it is no longer a possibility
                    # Set announced colour and rainbow to false
                    if colour_index == announced_colour_index or colour_index == len(card) - 1:
                        for rank in range(len(card[colour_index])):
                            card[colour_index][rank] *= 0

    def announce_rank(self, cards_indices, value):
        rank_index = value - 1
        for card_index in range(len(self.hand_knowledge)):
            card = self.hand_knowledge[card_index]
            if cards_indices is not None and card_index in cards_indices:
                # Card with this index has this rank
                for colour_index in range(len(card)):
                    # Set all ranks besides the announced rank to false
                    for rank in range(len(card[colour_index])):
                        if rank != rank_index:
                            card[colour_index][rank] *= 0
            else:
                # Card with this index does not have this rank
                for colour_index in range(len(card)):
                    # Set announced rank to false
                    card[colour_index][rank_index] *= 0

    ## ACTIVE GAME ACTIONS ##

    def HUMAN_player_selector(self, table):
        # print("Available players:")
        for player in table.player_list:
            if player is not self:
                # print("Player " + str(player.playerID) + ": " + str(player.print_hand()))
                player.print_hand(player.playerID)
        input_player = int(input("Which player to pick?"))
        if table.player_list[input_player] is self:
            print("You can't pick yourself.")
            self.HUMAN_player_selector(table)
        else:
            return table.player_list[input_player]

    def HUMAN_player_selector(self, table):
        print("Available players (with their hands):")
        for player in table.player_list:
            if player is not self:
                # print("Player " + str(player.playerID) + ": " + str(player.print_hand()))
                player.print_hand(player.playerID)
        print()

        while True:
            input_player = input("Which player to pick? ")
            if input_player.isdigit():
                input_player = int(input_player)
                if not input_player < 0 and not input_player > gameSettings.player_amount - 1:
                    if table.player_list[input_player] is not self:
                        return table.player_list[input_player]
                    else:
                        print("You can't pick yourself.")
                else:
                    print("Please pick a valid player.")
            else:
                print("Please enter a digit.")

    def HUMAN_colour_selector(self, table):
        print("Pick a colour: ", end='')
        # table.deck.print_colours_in_game()
        selected_colour = str(input())
        if selected_colour not in table.deck.colours_in_game or selected_colour == 'rainbow':
            print("Invalid colour, try again...")
            self.HUMAN_colour_selector(table)
        else:
            return str(selected_colour)

    def HUMAN_value_selector(self, table):
        while True:
            print("Pick a value (1-" + str(max(table.deck.values_in_game)) + "): ", end='')
            selected_value = input()
            if selected_value.isdigit():
                selected_value = int(selected_value)
                if not (max(table.deck.values_in_game) >= selected_value > 0):
                    print("Invalid value.")
                else:
                    return selected_value
            else:
                print("Please enter a digit.")

    def HUMAN_play_card(self, table):
        if gameSettings.show_own_hand:
            print("Current player has these cards:")
            self.print_hand()
        print("Current player has " + str(len(self.hand)) + " cards")
        table.print_piles()

        # Card input
        while True:
            input_card = input("Which card to play? (0-" + str(len(self.hand) - 1) + ")")
            if input_card.isdigit():
                input_card = int(input_card)
                if not input_card < 0 and not input_card > len(self.hand) - 1:
                    break
                else:
                    print("Please enter a valid digit.")
            else:
                print("Please enter a digit.")

        # Pile input
        while True:
            input_pile = input("Which pile to play to?")
            if input_pile.isdigit():
                input_pile = int(input_pile)
                if not input_pile < 0 and not input_pile > gameSettings.suit_amount - 1:
                    break
                else:
                    print("Please enter a valid digit.")
            else:
                print("Please enter a digit.")

        self.play_card(self.hand[input_card], table, input_pile)

    def play_card(self, card, table, pile_number):
        table.place_card(card, pile_number)
        # self.update_cards_left_representation(table, card) # Done in table.py
        index_card = self.hand.index(card)
        self.hand[index_card] = None
        # Take new card, if possible
        new_card = table.deck.get_new_card()
        if new_card is not None:
            self.hand[index_card] = new_card
            table.update_cards_left_representation_other_players(new_card, self)
            self.update_card_knowledge(index_card)

    def HUMAN_discard_card(self, table):
        if gameSettings.show_own_hand:
            print("Current player has these cards:")
            self.print_hand()
        print("Current player has " + str(len(self.hand)) + " cards")

        while True:
            input_card = input("Which card to discard? (0-" + str(len(self.hand) - 1) + ")")
            if input_card.isdigit():
                input_card = int(input_card)
                if not input_card < 0 and not input_card > int(len(self.hand) - 1):
                    self.discard_card(self.hand[input_card], table)
                    return
                else:
                    print("Invalid value.")
            else:
                print("Please enter a digit.")

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
            self.update_card_knowledge(index_card)

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
        player.announce_colour(cards_indices, colour, table)

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
        player.announce_rank(cards_indices, value)
        table.tokens.decrease_note_tokens()

    def HUMAN_pick_action(self, table):
        print("Player " + str(self.playerID) + ", pick an action:")

        while True:
            input_action = input(
                "Give a colour hint (0), give a value hint (1), discard a card (2) or play a card (3)")

            if input_action.isdigit():
                input_action = int(input_action)

                # Why are there no switch statements, Python..?
                if input_action is 0 and table.tokens.note_tokens > 0:
                    self.HUMAN_give_colour_hint(table)
                    break
                elif input_action is 1 and table.tokens.note_tokens > 0:
                    self.HUMAN_give_value_hint(table)
                    break
                elif input_action is 2:
                    if table.tokens.note_tokens < table.tokens.max_note_tokens:
                        self.HUMAN_discard_card(table)
                        break
                    else:
                        print("You can't discard: note tokens are maxed out.")
                elif input_action is 3:
                    self.HUMAN_play_card(table)
                    break
                else:
                    print("Invalid input or illegal move, try again...")
            else:
                print("Please input a digit.")

import gameSettings

class Player:
    def __init__(self, deck, playerID):
        self.hand = []
        self.playerID = playerID

        # Draw 4 cards
        for i in range(4):
            self.hand.append(deck.get_new_card())

        # Draw an additional card when <4 players
        if gameSettings.player_amount < 4:
            self.hand.append(deck.get_new_card())

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
        return table.player_list[input_player]

    def HUMAN_colour_selector(self, table):
        print("Pick a colour: ", end='')
        for colour in table.deck.colours_in_game:
            print(colour, end=' ')
        selected_colour = str(input())
        if selected_colour not in table.deck.colours_in_game:
            print("Invalid colour, try again...")
            self.HUMAN_colour_selector(table)
        else:
            return str(selected_colour)


    def HUMAN_play_card(self, table):
        print("Current player has these cards:")
        self.print_hand()
        input_card = int(input("Which card to play?"))
        table.print_piles()
        input_pile = int(input("Which pile to play to?"))
        self.play_card(self.hand[input_card], table, input_pile)

    def play_card(self, card, table, pile_number):
        table.place_card(card, pile_number)
        self.hand.remove(card)

    def HUMAN_discard_card(self, table):
        print("Current player has these cards:")
        self.print_hand()
        input_card = int(input("Which card to discard?"))
        self.discard_card(input_card, table)

    def discard_card(self, card, table):
        table.discard.add_to_discard(card)
        table.tokens.note_tokens -= 1 # TODO Should regain a token. Also check that max tokens isn't exceeded

    def HUMAN_give_colour_hint(self, table):
        selected_player = self.HUMAN_player_selector(table)
        selected_colour = self.HUMAN_colour_selector(table)
        self.give_colour_hint(selected_player, selected_colour)


    def give_colour_hint(self, player, colour):
        cards_indices = []
        index = 0
        for card in player.hand:
            if card.colour == colour:
                cards_indices.append(index)
            index += 1
        # For now, hints are just 'announced' as prints
        print("Player " + str(player.playerID) + ", you have the colour " + colour, end="")
        if not cards_indices:
            print(" nowhere.")
        else:
            print(" at card indices " + str(cards_indices))

    # TODO # Player actions
    #def give_hint:





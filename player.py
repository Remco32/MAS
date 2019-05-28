import gameSettings

class Player:
    def __init__(self, deck):
        self.hand = []

        # Draw 4 cards
        for i in range(4):
            self.hand.append(deck.get_new_card())

        # Draw an additional card when <4 players
        if gameSettings.player_amount < 4:
            self.hand.append(deck.get_new_card())

    def print_hand(self):
        i = 0
        for card in self.hand:
            print("Card " + str(i) + ": " + str(card.colour) + " " + str(card.value))
            i = i + 1

    def HUMAN_play_card(self, table):
        print("Current player has these cards:")
        self.print_hand()
        input_card = int(input("Which card to play?"))
        table.print_piles()
        input_pile = int(input("Which pile to play to?"))
        self.play_card(self.hand[input_card], table, input_pile)


    # TODO # Player actions
    #def give_hint:

    def discard_card(self, card, table):
        if table.tokens.note_tokens > 0:
            table.discard.add_to_discard(card)
        # TODO prevent player skipping his action in case he can't play it

    def play_card(self, card, table, pile_number):
        table.place_card(card, pile_number)
        self.hand.remove(card)

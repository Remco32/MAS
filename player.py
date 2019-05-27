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

    # TODO # Player actions
    #def give_hint:

    def discard_card(self, card, table):
        if table.tokens.note_tokens > 0:
            table.discard.add_to_discard(card)
        # TODO prevent player skipping his action in case he can't play it

    #def play_card(self, card):

import gameSettings
import random
def make_decision(player, table):
    decision, target_player, result = step_0(player, table)
    return decision, target_player, result

# Strategy 0: If there are no cards played and i has a card with rank 1 in hand and it knows that it has a card with rank 1 in hand, play that card.
# Return self, card index
def step_0(player, table):
    print("Check step 0")
    decision = 0
    target_player = player
    result = 0
    found_target = False
    if table.count_points() == 0:
        for i in range(len(player.hand)):
            if player.knows_rank(table, i) == 1:
                result = i
                found_target = True
    else:
        decision, target_player, result = step_1(player, table)

    if found_target is False:
        decision, target_player, result = step_1(player, table)

    return decision, target_player, result

# Strategy 1: If i has a playable card in hand and it knows that it has a playable card in hand, play that card.
# Return self, card index
def step_1(player, table):
    print("Check step 1")
    decision = 1
    target_player = player
    result = 0
    playable_cards = table.get_playable_cards()
    found_card = False
    for target in playable_cards:
        for i in range(len(player.hand)):
            card = player.knows_card(table, i)
            if card is not None:
                if card[0] == target[0] & card[1] == target[1]:
                    found_card = True
                    result = i
    if found_card == False:
        decision, target_player, result = step_2(player, table)

    return decision, target_player, result

# Strategy 2: If there is an available hint token and i+1 has a playable card in hand and it does not know that it has a playable card in hand but knows the suit of the playable card, give hint
# about the rank of the playable card.
# Return player, rank
def step_2(player, table):
    print("Check step 2")
    decision = 2
    target_player = table.player_list[(table.total_turn_counter + 1) % gameSettings.player_amount]
    result = 0
    if table.tokens.note_tokens > 0:
        playable_cards = table.get_playable_cards()
        hand = target_player.hand
        has_target = False
        for target in playable_cards:
            for card in hand:
                if target[0] == card.colour and target[1] == card.value and target_player.knows_card(table, hand.index(card)) is None:
                    if target_player.knows_colour(table, hand.index(card)) is not None:
                        has_target = True
                        result = target[1]
        if has_target == False:
            decision, target_player, result = step_3(player, table)
    else:
        decision, target_player, result = step_6(player, table)

    return decision, target_player, result

# Strategy 3: If there is an available hint token and i+1 has a playable card in hand and it does not know that it has a playable card in hand but knows the rank of the playable card, give hint
# about the suit of the playable card.
# Return player, suit
def step_3(player, table):
    print("Check step 3")
    decision = 3
    target_player = table.player_list[(table.total_turn_counter + 1) % gameSettings.player_amount]
    result = ''
    if table.tokens.note_tokens > 0:
        playable_cards = table.get_playable_cards()
        hand = target_player.hand
        has_target = False
        for target in playable_cards:
            for card in hand:
                if target[0] == card.colour and target[1] == card.rank and target_player.knows_card(table, hand.index(card)) is None:
                    if target_player.knows_rank(table, hand.index(card)) is not None:
                        has_target = True
                        result = target[0]
        if has_target == False:
            decision, target_player, result = step_4(player, table)
    else:
        decision, target_player, result = step_6(player, table)

    return decision, target_player, result

# Strategy 4: If there is an available hint token and i+2 has a playable card in hand and it does not know that it has a playable card in hand and does not know the rank or suit of the card, give
# a hint about either the suit or rank of the card.
# Return player, colour/rank
def step_4(player, table):
    print("Check step 4")
    decision = 4
    target_player = table.player_list[(table.total_turn_counter + 2) % gameSettings.player_amount]
    result = ''
    if table.tokens.note_tokens > 0 and len(gameSettings.player_amount > 2):
        playable_cards = table.get_playable_cards()
        hand = target_player.hand
        has_target = False
        for target in playable_cards:
            for card in hand:
                if target[0] == card.colour and target[1] == card.rank and target_player.knows_card(table, hand.index(card)) is None:
                    if target_player.knows_rank(table, hand.index(card)) is not None:
                        has_target = True
                        result = target[0]
                    elif target_player.knows_colour(table, hand.index(card)) is not None:
                        has_target = True
                        result = target[1]
        if has_target == False:
            decision, target_player, result = step_5(player, table)
    else:
        decision, target_player, result = step_6(player, table)

    return decision, target_player, result

# Strategy 5: If there is an available hint token and i+* has a card that is the final copy of that card in hand and it does not know it has the final copy of that card in hand, give a hint about
# the rank or colour of that card.
# Return player, card index
def step_5(player, table):
    print("Check step 5")
    decision = 5
    found_target = False
    if table.tokens.note_tokens > 0:
        for target_player in table.player_list:
            if target_player is not player:
                hand = target_player.hand
                for card in hand:
                    colour_index = table.deck.colours_in_game.index(card.colour)
                    rank_index = card.rank - 1
                    if player.cards_left_representation[colour_index][rank_index] == 1 and target_player.knows_card(table, hand.index(card)) is None:
                        found_target = True
                        if target_player.knows_rank(table, hand.index(card)) is None:
                            result = card.rank
                        elif target_player.knows_colour(table, hand.index(card)) is None:
                            result = card.colour

    else:
        decision, target_player, result = step_6(player, table)

    if found_target == False:
        decision, target_player, result = step_6(player, table)

    return decision, target_player, result

# Strategy 6: If i has a card in hand that has already been played and it knows that card, discard that card.
# Return self, card index
def step_6(player, table):
    print("Check step 6")
    decision = 6
    target_player = player
    result = 0
    if table.tokens.note_tokens < table.tokens.max_note_tokens:
        playable_cards = table.get_playable_cards()
        found_card = False
        for i in range(len(player.hand)):
            card = player.knows_card(table, i)
            if card is not None:
                for target in playable_cards:
                    if card[0] == target[0] and card[1] < target[1]:
                        found_card = True
                        result = i
    else:
        decision, target_player, result = step_6(player, table)
    if found_card == False:
        decision, target_player, result = step_6(player, table)

    return decision, target_player, result

# Strategy 7: If i has a non-playable card with suit x and rank y and it knows that this is not the only card with suit x and rank y in the game, discard that card.
# Return self, card index
def step_7(player, table):
    print("Check step 7")
    decision = 7
    target_player = player
    result = 0
    target_found = False
    if table.tokens.note_tokens < table.tokens.max_note_tokens:
        for i in range(len.player.hand):
            card = player.knows_card(table, i)
            if card is not None:
                rank_index = card[1] + 1
                colour_index = table.deck.colours_in_game.index(card[0])
                if player.cards_left_representation[colour_index][rank_index] > 1:
                    target_found = True
                    result = i

    if target_found == False:
        decision, target_player, result = step_8(player, table)

    return decision, target_player, result

# Strategy 8: If there are hint tokens left, give a random hint. If not, discard a random card
def step_8(player, table):
    print("Check step 8")
    decision = 8
    target_player = player
    if table.tokens.note_tokens > 0:
        decision = 80
        searching_target = True
        while searching_target:
            target_player = table.player_list[(table.total_turn_counter + 1) % gameSettings.player_amount]
            if target_player == player:
                # No useful hints, pick something random for the next player
                searching_target = False
                target_player = table.player_list[(table.total_turn_counter + 1) % gameSettings.player_amount]
                if random.randint(0,1) == 1:
                    # colour hint
                    result = table.deck.colours_in_game(random.randint(0, len(table.deck.colours_in_game)))
                else:
                    # rank hint
                    result = random.randint(table.deck.values_in_game[0], table.deck.values_in_game[-1])
            else:
                if random.randint(0, 1) == 1:
                    # colour hint
                    colours = []
                    for card_index in len(player.hand_knowledge):
                        for index in range(len(player.hand_knowledge[card_index])):
                            if sum(player.hand_knowledge[card_index][index]) > 1 and index not in colours:
                                colours.append(index)
                                searching_target = False
                    result = table.deck.colours_in_game[colours[random.randint(0,len(colours))]]
                else:
                    # rank hint
                    ranks = []
                    for card_index in range(len(player.hand_knowledge)):
                        rank_nos = list(zip(*target_player.hand_knowledge[card_index]))
                        for index in range(max(table.deck.values_in_game)):
                            if sum(rank_nos[index]) > 1 and index not in ranks:
                                searching_target = False
                                ranks.append(index + 1)
                    result = ranks[random.randint(0,len(ranks))]
    else:
        # TODO create smarter way to select card to discard i.e. make sure you don't discard something you know you still need
        decision = 81
        result = random.randint(0, len(player.hand))
    return decision, target_player, result
import table
import gameFlow as flow
import gameComponents
import player
import gameSettings


def play_game(table):
    flow.gameloop(table)


def TEST_completed_piles(table):
    colours_in_game = ['red', 'yellow', 'green', 'blue', 'white']

    i = -1
    for colour in colours_in_game:
        i += 1
        for value in range(1, 6):
            new_card = gameComponents.Card(colour, value)
            table.play_area[i].append(new_card)

    flow.gameloop(table)


def TEST_smaller_deck(table):
    # Generate special deck
    colours = ['red', 'yellow', 'green']
    values = [1, 2, 3, 4, 5]
    table.deck.colours_in_game = colours
    table.deck.values_in_game = values
    table.deck.generate_deck()

    # Remove players that got created using the old deck
    table.player_list.clear()

    # Generate new players with the new deck
    for i in range(gameSettings.player_amount):
        new_player = player.Player(table.deck, i, table)
        table.player_list.append(new_player)

    # Update representation after dealing cards
    for player_loop in table.player_list:
        for card in player_loop.hand:
            table.update_cards_left_representation_other_players(card, player_loop)
    table.current_player = table.player_list[table.total_turn_counter]
    flow.gameloop(table)




table = table.Table()
#play_game(table)
TEST_smaller_deck(table)
# TEST_completed_piles(table)

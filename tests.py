import table
import gameFlow as flow
import gameComponents


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


table = table.Table()
play_game(table)
# TEST_completed_piles(table)

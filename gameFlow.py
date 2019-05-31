import table

table = table.Table()
current_player_number = 0

current_player = table.player_list[current_player_number]
current_player.HUMAN_give_value_hint(table)

#current_player.play_card(current_player.hand[0], table, 0)

print()

def turn(current_player_number):
    current_player = table.player_list[current_player_number]


    current_player_number += 1

#TODO check for game fail state (0 storm tokens)
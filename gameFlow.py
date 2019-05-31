import table


def gameloop(table):
    while True:
        print()
        table.current_player.HUMAN_pick_action(table)

        if table.check_end_conditions() == -1:
            print("Game over, all storm tokens are flipped. 0 points are earned.")
            break
        if table.check_end_conditions() == 1:
            print("Game won. All piles filled correctly. 25 points are earned!")
            break
        if table.check_end_conditions() == 2:
            print("Final round!")
            final_round(table)
            table.count_points()
            break

        table.pass_turn()

def final_round(table):
    # Each player plays once more
    for i in range(len(table.player_list)):
        print()
        table.current_player.HUMAN_pick_action(table)
        table.pass_turn()


table = table.Table()
gameloop(table)
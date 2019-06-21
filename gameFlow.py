import table

def gameloop(table):
    print_welcome_text()

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
            print("The deck is empty. Final round!")
            final_round(table)
            print(str(table.count_points()) + " points were earned this game.")
            break

        table.pass_turn()


def final_round(table):
    # Each player plays once more
    for i in range(len(table.player_list)):
        print()
        table.current_player.HUMAN_pick_action(table)
        table.pass_turn()
    print()
    print("Game ended!")

def print_welcome_text():
    print("Welcome to Hanabi!")
    print("The goal of this game is to create a stack of cards that have the same colour, in ascending order.")
    print("You can't see your own hand, but can see that of your fellow players.")
    print("Game settings can be adjusted in gameSettings.py.")

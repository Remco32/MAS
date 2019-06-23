import table

def gameloop(table):
    print_welcome_text()

    while True:
        print()
        if table.player_list.index(table.current_player) is 0:
            table.current_player.HUMAN_pick_action(table)
        else:
            table.current_player.AGENT_pick_action(table)

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
    print("Welcome to Hanabi! To adjust game settings, please edit gameSettings.py.")
    print("The goal of this game is to create a stacks of cards that have the same colour, in ascending order.")
    print("You can't see your own hand, but can see that of your fellow players.")
    print("You can gather information about your hand by receiving hints."
          "Giving a hint costs one note token. One note token is replenished when a player discards a card.")
    print("When trying to play an invalid card, a storm token gets deducted."
          "When all storm tokens are gone, the game ends and the players lose.")
    print("To game otherwise ends when no more cards are in the game, or all stacks are completed.")

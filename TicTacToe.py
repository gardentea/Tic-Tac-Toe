import itertools
import random

letter_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
players = [1, 2]
board = []
number_filled_tiles = 0

def play_on():
    while True:
        again_response = input("The game is over, would you like to play again? (Y/N): ")
        if again_response[0].upper() == "Y":
            print("\nRestarting..")
            return True
        elif again_response[0].upper() == "N":
            print("\nGame has ended. Bye!")
            return False
        else:
            print("Invalid answer. Please try again.")

def win(current_game, player):
    global number_filled_tiles
    global board

    number_filled_tiles += 1

    def all_same(l, win_type):
        if l.count(l[0]) == len(l) and l[0] != 0:
            print(f"\nPlayer {player} is the winner {win_type}!")
            return True
        else:
            return False

    for row in board:
        if all_same(row, "horizontally (--)"):
            return True

    forward_diags = []
    for col, row in enumerate(reversed(range(len(board)))):
        forward_diags.append(board[row][col])
    if all_same(forward_diags, "diagonally (/)"):
        return True

    backwards_diags = []
    for ix in range(len(board)):
        backwards_diags.append(board[ix][ix])
    if all_same(backwards_diags, "diagonally (\\)"):
        return True

    for col in range(len(board)):
        check = []

        for row in board:
            check.append(row[col])
    
        if all_same(check, "vertically (|)"):
            return True
    
    if number_filled_tiles == (len(board) ** 2):
        print("\nThis game is a tie! No winners!")
        return True

    return False

def unoccupied_place (game_map, column, row):
    if game_map[row][column] == 0:
        return True
    else:
        return False

def computer_input_entry(game_map, player):
    dont_go_infinite_catch = 0

    while True:
        dont_go_infinite_catch += 1
        computer_column_choice = random.randrange(0, len(game_map), 1)
        computer_row_choice = random.randrange(0, len(game_map), 1)
        if unoccupied_place(game_map, computer_column_choice, computer_row_choice):
            break
        if dont_go_infinite_catch >= 1000:
            for i in range(len(game_map)):
                for n in range(len(game_map)):
                    if unoccupied_place(game_map, i, n):
                        # This is meant to find the first available empty spot and set the computer player to it
                        computer_column_choice = i
                        computer_row_choice = n

            print("Computer player broke down and had it's turn forced!")
            break
        
    print ("Computer player chooses: " + str(letter_array[computer_column_choice]) + " " + str(computer_row_choice + 1))
    game_map, played = game_board_placement(game_map, player, computer_column_choice, computer_row_choice)

def player_input_entry(game_map, player):
    while True:
        while True:
            while True: # This allows column_choice to be re-input by intentionally failing row_choice check, in case player inputs valid but undesired column choice.
                column_choice = (str(input(f"What column do you want to play? {[str(letter_array[i]) for i in range(len(game_map))]} ")))[0].upper()
                if column_choice in (str(letter_array[i]) for i in range(len(game_map))):
                    column_pre_conversion = column_choice
                    column_choice = letter_array.index(column_choice)
                    break
                else:
                    print("Input does not match available choices. Please try again.")

            row_choice = input(f"What row do you want to play? {[int(i + 1) for i in range(len(game_map))]} ")
            if row_choice.isdigit():
                row_choice = int(row_choice)
                if row_choice in (int(i + 1) for i in range(len(game_map))):
                    row_choice = row_choice - 1
                    break
                else:
                    print("Input does not match available choices. Please try again.") #Numbers out of bounds catch here
            else:
                print("Input does not match available choices. Please try again.") #Decimal numbers catch here
        
        if unoccupied_place(game_map, column_choice, row_choice):
            break
        else:
            print(f"\n{column_pre_conversion} {row_choice + 1} is not a free space. Please try again.")

    game_map = game_board_placement(game_map, player, column_choice, row_choice)

def game_board_placement(game_map, player=0, column=0, row=0, just_display=False):
    print("\n   "+"  ".join([str(letter_array[i]) for i in range(len(game_map))]))

    if not just_display:
        game_map[row][column] = player
    
    for count, column in enumerate(game_map):
        lettered_row = ""
        for item in column:
            if item == 0:
                lettered_row += "   "
            elif item == 1:
                lettered_row += ' X '
            elif item == 2:
                lettered_row += ' O '
        print(count + 1, lettered_row)

    return game_map, True

def make_the_board():
    global board
    global number_filled_tiles

    number_filled_tiles = 0 #Resetting from previous games

    while True:
        game_size = input("\nWhat size of Tic Tac Toe game would you like to play (Min: 2, Max: 7): " )
        if game_size.isdigit():
            game_size = int(game_size)
            if game_size <= 7 and game_size >= 2:
                print("Game size set to: " + str(game_size))
                break
            else:
                print("You entered a number that is out of bounds, please try again.")
        else:
            print("You did not enter a whole number, please try again.")    

    board = [[0 for i in range(game_size)] for i in range(game_size)]
    board, _ = game_board_placement(board, just_display=True)

def main_tic_tac_toe():

    while True:
        make_the_board()

        players = itertools.cycle([1, 2])

        while True:
            current_player = next(players)
            if current_player == 1:
                print("\nPlayer's turn!")
                player_input_entry(board, current_player)                  
            else:
                print("\nComputer's turn!")
                computer_input_entry(board, current_player)

            if win(board, current_player):
                break

        if not play_on():
            break

print("\nWelcome to Tic Tac Toe!")
main_tic_tac_toe()      
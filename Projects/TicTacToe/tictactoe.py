
#! Old Version

# from random import choice

# #? create board
# def show_board(board):
#     for row in board:
#         for col in row:
#             print(col, end="\t")
#         print("\n")

# #? set players
# def set_players():
#     player1 = choice(["X", "O"])
#     if player1 == "X":
#         player2 = "O"
#     else:
#         player2 = "X"
#     return player1, player2



# #? Take input

# def take_input(board, player):
#     while True:
#         player_input = input("Please Enter a number between 1, 9 represents an empty position:     ")
#         if player_input == "1" and board[0][0].isdigit():
#             board[0][0] = player
#             break
#         elif player_input == "2" and board[0][1].isdigit():
#             board[0][1] = player
#             break
#         elif player_input == "3" and board[0][2].isdigit():
#             board[0][2] = player
#             break
#         elif player_input == "4" and board[1][0].isdigit():
#             board[1][0] = player
#             break
#         elif player_input == "5" and board[1][1].isdigit():
#             board[1][1] = player
#             break
#         elif player_input == "6" and board[1][2].isdigit():
#             board[1][2] = player
#             break
#         elif player_input == "7" and board[2][0].isdigit():
#             board[2][0] = player
#             break
#         elif player_input == "8" and board[2][1].isdigit():
#             board[2][1] = player
#             break
#         elif player_input == "9" and board[2][2].isdigit():
#             board[2][2] = player
#             break
#         else:
#             print("Invalid input!!")
#             continue


# #? Chsck full board
# def Check_Full_board(board):
#     for row in board:
#         for col in row:
#             if col.isdigit():
#                 return False
#     return True


# #? check win
# def check_win(board):
#     return  board[0][0] == board[0][1] == board[0][2] or \
#             board[1][0] == board[1][1] == board[1][2] or \
#             board[2][0] == board[2][1] == board[2][2] or \
#             board[0][0] == board[1][0] == board[2][0] or \
#             board[0][1] == board[1][1] == board[2][1] or \
#             board[0][2] == board[1][2] == board[2][2] or \
#             board[0][0] == board[1][1] == board[2][2] or \
#             board[0][2] == board[1][1] == board[2][0]



# #? Let's play
# def play():
#     player1, player2 = set_players()
#     print(f"Player1 : {player1}")
#     print(f"Player2 : {player2}")
#     board = [
#         [1, 2, 3],
#         [4, 5, 6],
#         [7, 8, 9]
#     ]
#     show_board(board=board)

#     while True:
#         for player in [player1, player2]:
#             print(f"{player} Turn")
#             take_input(board= board, player= player)
#             if check_win(board=board):
#                 print(f"Player: {player} Wins!!!")
#                 break
#             if Check_Full_board(board= board):
#                 print("Game Ends With draw!!")
#                 break
#             if check_win(board= board):
#                 break
#             if Check_Full_board(board= board):
#                 break



# if __name__ == "__main__":
#     play()





#todo: New Version

from random import choice


# ============================================================
# Create Board
# ============================================================

def create_board():
    return [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]


# ============================================================
# Show Board
# ============================================================

def show_board(board):
    for row in board:
        print("\t".join(map(str, row)))
    print()


# ============================================================
# Set Players
# ============================================================

def set_players():
    player1 = choice(["X", "O"])
    player2 = "O" if player1 == "X" else "X"

    return player1, player2


# ============================================================
# Take Player Input
# ============================================================

def take_input(board, player):
    while True:
        player_input = input(
            "Please enter a number between 1 and 9 "
            "that represents an empty position: "
        )

        if not player_input.isdigit():
            print("Invalid input!! Please enter a number.")
            continue

        position = int(player_input)

        if position < 1 or position > 9:
            print("Invalid input!! Please enter a number between 1 and 9.")
            continue

        index = position - 1

        row = index // 3
        col = index % 3

        if not str(board[row][col]).isdigit():
            print("This position is already taken!!")
            continue

        board[row][col] = player
        break


# ============================================================
# Check Full Board
# ============================================================

def check_full_board(board):
    for row in board:
        for col in row:
            if str(col).isdigit():
                return False

    return True


# ============================================================
# Check Winner
# ============================================================

def check_win(board):
    winning_combinations = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],

        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],

        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for combination in winning_combinations:
        values = [
            board[row][col]
            for row, col in combination
        ]

        if values[0] == values[1] == values[2]:
            return True

    return False


# ============================================================
# Play Game
# ============================================================

def play():
    player1, player2 = set_players()
    players = [player1, player2]

    board = create_board()

    print(f"Player 1: {player1}")
    print(f"Player 2: {player2}")
    print()

    show_board(board)

    while True:

        for player in players:

            print(f"{player}'s Turn")

            take_input(board, player)
            show_board(board)

            if check_win(board):
                print(f"Player {player} Wins!!!")
                return

            if check_full_board(board):
                print("Game Ends With a Draw!!")
                return


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    play()





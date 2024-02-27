import os
import time

def print_board(board):
    print("          Player 2")
    print(" ")
    print("   " + "  ".join([f'{i: <2}' for i in board[7:13][::-1]]))
    print(f'{board[13]: <2}', " " * 22, f'{board[6]: <2}')
    print("   " + "  ".join([f'{i: <2}' for i in board[0:6]]))
    print(" ")
    print("          Player 1")
    print(" ")

def is_valid_move(board, player, pit):
    return board[pit] != 0 and (player == 0 and 0 <= pit <= 5) or (player == 1 and 7 <= pit <= 12)

def make_move(board, player, pit):
    stones = board[pit]
    board[pit] = 0
    last_pit = pit  # Set last_pit to initial value of pit
    while stones > 0:
        pit = (pit + 1) % 14
        if pit == 6 and player == 1 or pit == 13 and player == 0:
            continue
        board[pit] += 1
        stones -= 1
        last_pit = pit
    return last_pit

def capture_opposite(board, player, pit):
    if board[pit] == 1 and (player == 0 and 0 <= pit <= 5) or (player == 1 and 7 <= pit <= 12):
        opposite_pit = 12 - pit
        if board[opposite_pit] > 0:
            board[6 if player == 0 else 13] += board[opposite_pit] + 1
            board[opposite_pit] = board[pit] = 0

def is_game_over(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0

def get_winner(board):
    if board[6] > board[13]:
        return 1
    elif board[6] < board[13]:
        return 2
    else:
        return 0

# Initial game state
board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
current_player = 0

while not is_game_over(board):
    print_board(board)
    pit = -1
    while True:
        try:
            pit_input = input(f"Player {current_player + 1}, choose your pit: ")
            pit = int(pit_input) - 1
            if not is_valid_move(board, current_player, pit):
                print("Invalid move. Please choose a valid pit on your side.")
            else:
                break
        except ValueError:
            print(f"Invalid input '{pit_input}', please enter a number.")
    last_pit = make_move(board, current_player, pit)
    capture_opposite(board, current_player, last_pit)
    if last_pit != (6 if current_player == 0 else 13):
        current_player = 1 - current_player

winner = get_winner(board)
if winner == 0:
    print("The game is a draw.")
else:
    print(f"Player {winner} wins!")
# DONE: Flyt alle konstanter ud i global scope
PLAYER_ONE = 0
PLAYER_TWO = 1
PLAYER_ONE_GOAL = 6
PLAYER_TWO_GOAL = 13
PLAYER_ONE_PITS = range(0, 6)
PLAYER_TWO_PITS = range(7, 13)

board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
current_player = PLAYER_ONE

# DONE: Tilføj (AI) til player 2 hvis game_mode == 2
def print_board(board, game_mode):
    print("          Player 2" + (" (AI)" if game_mode == "2" else ""))
    print(" ")
    print("   " + "  ".join([f'{i: <2}' for i in board[7:13][::-1]]))
    print(f'{board[13]: <2}', " " * 22, f'{board[6]: <2}')
    print("   " + "  ".join([f'{i: <2}' for i in board[0:6]]))
    print(" ")
    print("          Player 1")
    print(" ")

# DONE: Fix is_valid_move så man ikke kan tage fra huller med 0 sten
def is_valid_move(board, player, pit):
    if not ((player == PLAYER_ONE and pit in PLAYER_ONE_PITS) or (player == PLAYER_TWO and pit in PLAYER_TWO_PITS)):
        print("Invalid move. Please choose a valid pit on your side.")
        return False
    if board[pit] == 0:
        print("Warning: You've selected a pit with 0 stones. Please choose a different pit.")
        return False
    return True

def is_game_over(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0

def get_winner(board):
    if board[PLAYER_ONE_GOAL] > board[PLAYER_TWO_GOAL]:
        return 1
    elif board[PLAYER_ONE_GOAL] < board[PLAYER_TWO_GOAL]:
        return 2
    else:
        return 0

# This function makes a move and returns the last pit that a stone was dropped into
def make_move(board, player, pit):
    stones = board[pit]
    board[pit] = 0
    last_pit = pit
    while stones > 0:
        pit = (pit + 1) % 14
        if pit == PLAYER_ONE_GOAL and player == PLAYER_TWO or pit == PLAYER_TWO_GOAL and player == PLAYER_ONE:
            continue
        board[pit] += 1
        stones -= 1
        last_pit = pit
    return last_pit

def capture_opposite(board, player, pit):
    if (player == PLAYER_ONE and pit in PLAYER_ONE_PITS) or (player == PLAYER_TWO and pit in PLAYER_TWO_PITS):
        opposite_pit = 12 - pit
        if board[pit] == 1 and board[opposite_pit] > 0:
            board[PLAYER_ONE_GOAL if player == PLAYER_ONE else PLAYER_TWO_GOAL] += board[opposite_pit] + 1
            board[opposite_pit] = board[pit] = 0

def minimax(board, player, depth, alpha, beta):
    if depth == 0 or is_game_over(board):
        return board[PLAYER_ONE_GOAL] - board[PLAYER_TWO_GOAL]
    if player == PLAYER_ONE:
        max_eval = float('-inf')
        for pit in PLAYER_ONE_PITS:
            if board[pit] > 0:
                new_board = board[:]
                last_pit = make_move(new_board, player, pit)
                capture_opposite(new_board, player, last_pit)
                eval = minimax(new_board, PLAYER_TWO, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for pit in PLAYER_TWO_PITS:
            if board[pit] > 0:
                new_board = board[:]
                last_pit = make_move(new_board, player, pit)
                capture_opposite(new_board, player, last_pit)
                eval = minimax(new_board, PLAYER_ONE, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def get_ai_move(board, player, depth=5):
    best_move = -1
    alpha = float('-inf')
    beta = float('inf')
    best_eval = alpha if player == PLAYER_ONE else beta
    for pit in PLAYER_ONE_PITS if player == PLAYER_ONE else PLAYER_TWO_PITS:
        if board[pit] > 0:
            new_board = board[:]
            last_pit = make_move(new_board, player, pit)
            capture_opposite(new_board, player, last_pit)
            eval = minimax(new_board, 1 - player, depth - 1, alpha, beta)
            if player == PLAYER_ONE and eval > best_eval or player == PLAYER_TWO and eval < best_eval:
                best_eval = eval
                best_move = pit
    return best_move

game_mode = input("Choose game mode (1 - Player vs Player, 2 - Player vs AI): ")
while game_mode not in ["1", "2"]:
    game_mode = input("Invalid input. Choose game mode (1 - Player vs Player, 2 - Player vs AI): ")

while not is_game_over(board):
    print_board(board, game_mode)
    pit = -1
    if game_mode == "1" or current_player == PLAYER_ONE:
        while True:
            try:
                pit_input = input(f"Player {current_player + 1}, choose your pit: ")
                pit = int(pit_input) - 1
                if current_player == PLAYER_TWO:
                    pit += 7 
                if not is_valid_move(board, current_player, pit):
                    continue
                else:
                    break
            except ValueError:
                print(f"Invalid input '{pit_input}', please enter a number.")
    else:
        pit = get_ai_move(board, current_player)
        print(f"AI chooses pit: {pit + 1}")
    last_pit = make_move(board, current_player, pit)
    capture_opposite(board, current_player, last_pit)
    if last_pit not in [6, 13]:
        current_player = 1 - current_player

print_board(board, game_mode)
winner = get_winner(board)
if winner == 0:
    print("The game is a draw.")
else:
    print(f"Player {winner} wins!")
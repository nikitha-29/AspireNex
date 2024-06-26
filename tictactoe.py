import math

# Define the board
board = [' ' for _ in range(9)]

def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_board_full(board):
    return ' ' not in board

def minimax(board, depth, alpha, beta, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, alpha, beta, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, alpha, beta, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            move_val = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        human_move = int(input("Enter your move (1-9): ")) - 1
        if board[human_move] != ' ':
            print("Invalid move. Try again.")
            continue
        board[human_move] = 'X'
        print_board(board)

        if check_winner(board, 'X'):
            print("Congratulations! You win!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

        print("AI's turn...")
        ai_move = best_move(board)
        board[ai_move] = 'O'
        print_board(board)

        if check_winner(board, 'O'):
            print("AI wins!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

play_game()

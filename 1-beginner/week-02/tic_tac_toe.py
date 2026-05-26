"""
    Create a Python program that simulates a simple AI agent
    that can learn to play tic-tac-toe. The program must Define
    the game board, Check if a player has won, Check if the game
    is a tie, Main game loop, Call the main game loop
"""

def create_board():
    return [' '] * 9  # 9 empty spaces

def print_board(board: list):
    print()
    for i in range(3):
        row = board[i*3 : i*3 + 3]
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---|---|---")
    print()

def check_winner(board: list, player: str):
    win_conditions = [
        [0, 1, 2],  # top row
        [3, 4, 5],  # middle row
        [6, 7, 8],  # bottom row
        [0, 3, 6],  # left column
        [1, 4, 7],  # middle column
        [2, 5, 8],  # right column
        [0, 4, 8],  # diagonal top-left to bottom-right
        [2, 4, 6],  # diagonal top-right to bottom-left
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_tie(board: list):
    return ' ' not in board

def minimax(board, is_maximizing: bool):
    if check_winner(board, 'O'):   # AI wins
        return 1
    if check_winner(board, 'X'):   # Human wins
        return -1
    if check_tie(board):           # Tie
        return 0

    if is_maximizing:  # AI's turn — Maximizing score
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:              # Human's turn — Minimizing Score
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def ai_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = 'O'
    print(f"AI chose position {best_move}")

def main():
    board = create_board()
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    print("Positions are numbered 0-8 (left to right, top to bottom):")
    print_board([str(i) for i in range(9)])  # Show position guide

    while True:
        # Human's turn
        print_board(board)
        while True:
            try:
                move = int(input("Enter your move (0-8): "))
                if board[move] == ' ':
                    board[move] = 'X'
                    break
                else:
                    print("That spot is taken! Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Enter a number between 0 and 8.")

        if check_winner(board, 'X'):
            print_board(board)
            print("Congratulations! You win!")
            break
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            break

        # AI's turn
        print("AI is thinking...")
        ai_move(board)

        if check_winner(board, 'O'):
            print_board(board)
            print("AI wins! Better luck next time.")
            break
        if check_tie(board):
            print_board(board)
            print("It's a tie!")
            break


# --- 6. CALL THE MAIN GAME LOOP ---
if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
import random

# Function to check if a player has won
def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def is_board_full(board):
    return all(all(cell != '' for cell in row) for row in board)

# Minimax algorithm for the AI player
def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'):
        return -1
    if check_win(board, 'O'):
        return 1
    if is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_eval = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                eval = minimax(board, 0, False)
                board[i][j] = ''
                if eval > best_eval:
                    best_eval = eval
                    move = (i, j)
    return move

# Function to handle the player's move
def player_move(row, col):
    if board[row][col] == '' and not game_over:
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state='disabled')
        if check_win(board, 'X'):
            messagebox.showinfo('Tic-Tac-Toe', 'You win!')
            end_game()

        if not is_board_full(board):
            ai_row, ai_col = best_move(board)
            board[ai_row][ai_col] = 'O'
            buttons[ai_row][ai_col].config(text='O', state='disabled')
            if check_win(board, 'O'):
                messagebox.showinfo('Tic-Tac-Toe', 'AI wins!')
                end_game()
        elif is_board_full(board):
            messagebox.showinfo('Tic-Tac-Toe', 'It\'s a tie!')
            end_game()	

# Function to reset the game
def reset_game():
    global board, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state='active')
    game_over = False

# Function to end the game
def end_game():
    global game_over
    game_over = True
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state='disabled')

# Create the main window
window = tk.Tk()
window.title('Tic-Tac-Toe')

# Create buttons for the game board
buttons = [[None, None, None] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(window, text='', width=10, height=3, command=lambda row=i, col=j: player_move(row, col))
        buttons[i][j].grid(row=i, column=j)

# Create a Reset button
reset_button = tk.Button(window, text='Reset', width=10, height=2, command=reset_game)
reset_button.grid(row=3, column=1)

# Initialize the game board
board = [['' for _ in range(3)] for _ in range(3)]
game_over = False

# Start the GUI main loop
window.mainloop()

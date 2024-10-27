import random
import tkinter as tk
from tkinter import font

def is_valid(board, row, col, num):
    # Prüfe, ob die Nummer in der Reihe bereits existiert
    for i in range(9):
        if board[row][i] == num:
            return False

    # Prüfe, ob die Nummer in der Spalte bereits existiert
    for i in range(9):
        if board[i][col] == num:
            return False

    # Prüfe, ob die Nummer im 3x3-Block bereits existiert
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def solve_and_count(board):
    count = [0]
    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            solve(board)
                            board[row][col] = 0
                    return
        count[0] += 1
    solve(board)
    return count[0]

def remove_numbers(board, num_holes):
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    while num_holes > 0 and cells:
        row, col = cells.pop()
        backup = board[row][col]
        board[row][col] = 0
        # Prüfe, ob das Rätsel immer noch eine eindeutige Lösung hat
        if solve_and_count([row[:] for row in board]) != 1:
            board[row][col] = backup
        else:
            num_holes -= 1

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    # Fülle alle 3x3-Blöcke der Hauptdiagonalen, um die Startbedingungen zu setzen
    for block in range(3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        start_row, start_col = 3 * block, 3 * block
        for row in range(3):
            for col in range(3):
                board[start_row + row][start_col + col] = nums.pop()

    # Löse das Sudoku komplett
    solve_board(board)
    
    # Entferne eine bestimmte Anzahl an Feldern, um ein Rätsel zu erstellen
    remove_numbers(board, num_holes=40)

    return board

def show_board_in_window(board):
    root = tk.Tk()
    root.title("Sudoku Rätsel")
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    my_font = font.Font(size=20)

    for i in range(9):
        for j in range(9):
            value = board[i][j] if board[i][j] != 0 else ""
            entry = tk.Entry(frame, width=2, font=my_font, justify='center', relief='solid', bd=1)
              # Set height to make the entry box square
            if i % 3 == 0 and i != 0:
                pady = (4, 1)  # Dickere horizontale Linie nach jedem 3er Block
            else:
                pady = (2 if i % 3 == 0 else 1)

            if j % 3 == 0 and j != 0:
                padx = (4, 1)  # Dickere vertikale Linie nach jedem 3er Block
            else:
                padx = (2 if j % 3 == 0 else 1)

            entry.grid(row=i, column=j, padx=padx, pady=pady)
            entry.insert(0, value)
            entry.config(state='disabled' if board[i][j] != 0 else 'normal')

    root.mainloop()

def main():
    sudoku_board = generate_sudoku()
    show_board_in_window(sudoku_board)

if __name__ == "__main__":
    main()




import random
import tkinter as tk
from tkinter import font, messagebox
import pickle

# Sudoku-Validierungsfunktionen
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# Sudoku-Lösungsfunktionen
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
        if solve_and_count([row[:] for row in board]) != 1:
            board[row][col] = backup
        else:
            num_holes -= 1

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for block in range(3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        start_row, start_col = 3 * block, 3 * block
        for row in range(3):
            for col in range(3):
                board[start_row + row][start_col + col] = nums.pop()
    solve_board(board)
    remove_numbers(board, num_holes=40)
    return board

# Funktionen zum Speichern und Laden des Spielstands
def save_game(board):
    with open("sudoku_save.pkl", "wb") as file:
        pickle.dump(board, file)
    messagebox.showinfo("Spiel gespeichert", "Das Spiel wurde erfolgreich gespeichert.")

def load_game():
    try:
        with open("sudoku_save.pkl", "rb") as file:
            board = pickle.load(file)
        messagebox.showinfo("Spiel geladen", "Das Spiel wurde erfolgreich geladen.")
        return board
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Kein gespeicherter Spielstand gefunden.")
        return generate_sudoku()

# GUI-Funktionen
def show_board_in_window(board):
    root = tk.Tk()
    root.title("Sudoku Rätsel")
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    my_font = font.Font(size=20)
    selected_number = tk.StringVar()
    entries = []

    for i in range(9):
        row_entries = []
        for j in range(9):
            value = board[i][j] if board[i][j] != 0 else ""
            entry = tk.Entry(frame, width=2, font=my_font, justify='center', relief='solid', bd=1)
            pady = (4, 1) if i % 3 == 0 and i != 0 else (1, 1)
            padx = (4, 1) if j % 3 == 0 and j != 0 else (1, 1)
            entry.grid(row=i, column=j, padx=padx, pady=pady)
            entry.insert(0, value)
            entry.config(state='disabled' if board[i][j] != 0 else 'normal')
            row_entries.append(entry)
        entries.append(row_entries)

    def on_number_click(num):
        selected_number.set(num)
        for i in range(9):
            for j in range(9):
                if entries[i][j].get() == str(num):
                    entries[i][j].config(fg='blue')
                elif entries[i][j].cget('state') == 'disabled':
                    entries[i][j].config(fg='black')

    def on_entry_click(event):
        if selected_number.get():
            row, col = event.widget.grid_info()['row'], event.widget.grid_info()['column']
            num = int(selected_number.get())
            if is_valid([[int(e.get()) if e.get() else 0 for e in row] for row in entries], row, col, num):
                current_value = event.widget.get()
                if current_value == "" or event.widget.cget('fg') != 'blue':
                    event.widget.delete(0, tk.END)
                    event.widget.insert(0, selected_number.get())
                    event.widget.config(fg='blue')
            else:
                messagebox.showerror("Ungültige Eingabe", f"Die Zahl {num} an Position ({row + 1}, {col + 1}) verstößt gegen die Sudoku-Regeln.")
                event.widget.config(bg='red')
                root.after(1000, lambda: event.widget.config(bg='white'))

    for row in entries:
        for entry in row:
            if entry.cget('state') == 'normal':
                entry.bind("<Button-1>", on_entry_click)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    for num in range(1, 10):
        button = tk.Button(button_frame, text=str(num), font=my_font, width=2, command=lambda n=num: on_number_click(n))
        button.pack(side=tk.LEFT, padx=5)

    def save_button_click():
        current_board = [[int(e.get()) if e.get() else 0 for e in row] for row in entries]
        save_game(current_board)

    def load_button_click():
        loaded_board = load_game()
        if loaded_board:
            root.destroy()
            show_board_in_window(loaded_board)

    save_button = tk.Button(root, text="Speichern", command=save_button_click)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    load_button = tk.Button(root, text="Laden", command=load_button_click)
    load_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()

def main():
    sudoku_board = load_game() if messagebox.askyesno("Spiel laden", "Möchtest du ein gespeichertes Spiel laden?") else generate_sudoku()
    show_board_in_window(sudoku_board)

if __name__ == "__main__":
    main()


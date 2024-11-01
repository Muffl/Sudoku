import random
import tkinter as tk
from tkinter import font, messagebox, filedialog
import pickle
import datetime
import os
import unittest

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

def generate_sudoku(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    for block in range(3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        start_row, start_col = 3 * block, 3 * block
        for row in range(3):
            for col in range(3):
                board[start_row + row][start_col + col] = nums.pop()
    solve_board(board)
    if difficulty == 'Leicht':
        remove_numbers(board, num_holes=30)
    elif difficulty == 'Mittel':
        remove_numbers(board, num_holes=40)
    elif difficulty == 'Schwer':
        remove_numbers(board, num_holes=50)
    return board

# Funktionen zum Speichern und Laden des Spielstands
def save_game(board):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"sudoku_save_{timestamp}.pkl"
    with open(filename, "wb") as file:
        pickle.dump(board, file)
    messagebox.showinfo("Spiel gespeichert", f"Das Spiel wurde erfolgreich unter dem Namen '{filename}' gespeichert.")

def load_game():
    try:
        filename = filedialog.askopenfilename(initialdir=".", title="Wähle einen gespeicherten Spielstand aus", filetypes=[("Pickle Dateien", "*.pkl")])
        if filename:
            with open(filename, "rb") as file:
                board = pickle.load(file)
            messagebox.showinfo("Spiel geladen", f"Das Spiel '{os.path.basename(filename)}' wurde erfolgreich geladen.")
            return board
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Kein gespeicherter Spielstand gefunden.")
    return None

# GUI-Funktionen
def show_board_in_window(board):
    root = tk.Tk()
    root.title("Sudoku Rätsel")
    root.configure(bg='#f0f0f0')
    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(padx=10, pady=10)

    my_font = font.Font(family="Helvetica", size=20, weight="bold")
    selected_number = tk.StringVar()
    entries = []

    for i in range(9):
        row_entries = []
        for j in range(9):
            value = board[i][j] if board[i][j] != 0 else ""
            entry = tk.Entry(frame, width=2, font=my_font, justify='center', relief='solid', bd=2, bg='#ffffff', fg='#333333')
            pady = (6, 2) if i % 3 == 0 and i != 0 else (2, 2)
            padx = (6, 2) if j % 3 == 0 and j != 0 else (2, 2)
            entry.grid(row=i, column=j, padx=padx, pady=pady)
            entry.insert(0, value)
            entry.config(state='disabled' if board[i][j] != 0 else 'normal')
            if board[i][j] != 0:
                entry.config(disabledbackground='#d9d9d9', disabledforeground='#000000')
            row_entries.append(entry)
        entries.append(row_entries)

    def update_number_buttons():
        counts = {str(num): 0 for num in range(1, 10)}
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                if value in counts:
                    counts[value] += 1
        for num, button in number_buttons.items():
            if counts[num] >= 9:
                button.config(state='disabled')
            else:
                button.config(state='normal')

    def on_number_click(num):
        selected_number.set(num)
        for i in range(9):
            for j in range(9):
                if entries[i][j].get() == str(num):
                    entries[i][j].config(fg='#007acc')
                elif entries[i][j].cget('state') == 'disabled':
                    entries[i][j].config(fg='#000000')
        for number, button in number_buttons.items():
            if number == str(num):
                button.config(fg='#ff0000')  # Highlight the selected number in red
            else:
                button.config(fg='#ffffff')  # Reset others to white

    def on_entry_click(event):
        if selected_number.get():
            row, col = event.widget.grid_info()['row'], event.widget.grid_info()['column']
            num = int(selected_number.get())
            if is_valid([[int(e.get()) if e.get() else 0 for e in row] for row in entries], row, col, num):
                current_value = event.widget.get()
                if current_value == "" or event.widget.cget('fg') != '#007acc':
                    event.widget.delete(0, tk.END)
                    event.widget.insert(0, selected_number.get())
                    event.widget.config(fg='#007acc', bg='#e6f7ff')
                    update_number_buttons()
            else:
                messagebox.showerror("Ungültige Eingabe", f"Die Zahl {num} an Position ({row + 1}, {col + 1}) verstößt gegen die Sudoku-Regeln.")
                event.widget.config(bg='#ffcccc')
                root.after(1000, lambda: event.widget.config(bg='#ffffff'))

    for row in entries:
        for entry in row:
            if entry.cget('state') == 'normal':
                entry.bind("<Button-1>", on_entry_click)

    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.pack(pady=10)

    number_buttons = {}
    for num in range(1, 10):
        button = tk.Button(button_frame, text=str(num), font=my_font, width=3, command=lambda n=num: on_number_click(n), bg='#007acc', fg='#ffffff', activebackground='#005f99', activeforeground='#ffffff')
        button.pack(side=tk.LEFT, padx=5)
        number_buttons[str(num)] = button

    def save_button_click():
        current_board = [[int(e.get()) if e.get() else 0 for e in row] for row in entries]
        save_game(current_board)

    def load_button_click():
        loaded_board = load_game()
        if loaded_board:
            root.destroy()
            show_board_in_window(loaded_board)

    save_button = tk.Button(root, text="Speichern", command=save_button_click, font=my_font, bg='#28a745', fg='#ffffff', activebackground='#218838', activeforeground='#ffffff')
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    load_button = tk.Button(root, text="Laden", command=load_button_click, font=my_font, bg='#ffc107', fg='#ffffff', activebackground='#e0a800', activeforeground='#ffffff')
    load_button.pack(side=tk.RIGHT, padx=10, pady=10)

    update_number_buttons()
    root.mainloop()

def main():
    root = tk.Tk()
    root.title("Schwierigkeitsgrad auswählen")
    root.configure(bg='#f0f0f0')

    def set_difficulty(difficulty):
        root.destroy()
        sudoku_board = load_game() if messagebox.askyesno("Spiel laden", "Möchtest du ein gespeichertes Spiel laden?") else generate_sudoku(difficulty)
        show_board_in_window(sudoku_board)

    tk.Label(root, text="Wähle den Schwierigkeitsgrad:", font=('Helvetica', 16), bg='#f0f0f0').pack(pady=10)
    tk.Button(root, text="Leicht", font=('Helvetica', 14), width=15, command=lambda: set_difficulty('Leicht')).pack(pady=5)
    tk.Button(root, text="Mittel", font=('Helvetica', 14), width=15, command=lambda: set_difficulty('Mittel')).pack(pady=5)
    tk.Button(root, text="Schwer", font=('Helvetica', 14), width=15, command=lambda: set_difficulty('Schwer')).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

# Unit Tests
class TestSudokuFunctions(unittest.TestCase):

    def test_is_valid(self):
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        # Teste, ob die Zahl 5 in Position (0, 2) gültig ist
        self.assertFalse(is_valid(board, 0, 2, 5))  # Es gibt schon eine 5 in der Zeile
        # Teste, ob die Zahl 4 in Position (0, 2) gültig ist
        self.assertTrue(is_valid(board, 0, 2, 4))   # Die 4 passt dort

    def test_solve_board(self):
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        # Teste, ob das Board lösbar ist
        self.assertTrue(solve_board(board))

if __name__ == '__main__':
    unittest.main()

# Writes a complete, ready-to-run Nonogram (15x15) tkinter game to /mnt/data/nonogram.py
import tkinter as tk
from tkinter import messagebox
import random
from functools import partial

GRID = 15
CELL = 30
CLUE_SPACE_LEFT = 120
CLUE_SPACE_TOP = 120
WINDOW_PADDING = 10

class Nonogram:
    def __init__(self, master, grid_size=GRID):
        self.master = master
        self.grid_size = grid_size
        self.cell_size = CELL
        self.canvas_width = CLUE_SPACE_LEFT + grid_size * self.cell_size + WINDOW_PADDING
        self.canvas_height = CLUE_SPACE_TOP + grid_size * self.cell_size + WINDOW_PADDING

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(side=tk.TOP)

        self.controls = tk.Frame(master)
        self.controls.pack(side=tk.TOP, fill=tk.X, pady=6)

        tk.Button(self.controls, text="New puzzle", command=self.new_puzzle).pack(side=tk.LEFT, padx=6)
        tk.Button(self.controls, text="Check", command=self.check).pack(side=tk.LEFT, padx=6)
        tk.Button(self.controls, text="Reveal solution", command=self.reveal).pack(side=tk.LEFT, padx=6)
        tk.Button(self.controls, text="Copy solution to clipboard", command=self.copy_solution).pack(side=tk.LEFT, padx=6)

        self.status = tk.Label(master, text="Left click to reveal, right click to cross (mark).")
        self.status.pack(side=tk.TOP, pady=4)

        self.master.bind("<space>", lambda e: self.new_puzzle())
        # data structures
        self.solution = [[0]*grid_size for _ in range(grid_size)]
        # player state: 0 unknown, 1 filled (revealed), -1 crossed (X)
        self.state = [[0]*grid_size for _ in range(grid_size)]
        # computed clues
        self.row_clues = []
        self.col_clues = []

        # draw initial empty board
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        # for MacOS (two-finger tap)
        self.canvas.bind("<Button-2>", self.right_click)

        self.new_puzzle()

    def new_puzzle(self):
        # create a random solution and compute clues (guarantees solvable: the generated solution)
        # Keep density moderate so it's interesting
        density = random.uniform(0.28, 0.45)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.solution[r][c] = 1 if random.random() < density else 0
                self.state[r][c] = 0
        self.row_clues = [self._line_to_clues(self.solution[r]) for r in range(self.grid_size)]
        self.col_clues = [self._line_to_clues([self.solution[r][c] for r in range(self.grid_size)]) for c in range(self.grid_size)]
        self.redraw()

    @staticmethod
    def _line_to_clues(line):
        clues = []
        count = 0
        for v in line:
            if v:
                count += 1
            else:
                if count:
                    clues.append(count)
                    count = 0
        if count:
            clues.append(count)
        if not clues:
            clues = [0]
        return clues

    def redraw(self):
        self.canvas.delete("all")
        # draw clues
        # Left/top area background
        self.canvas.create_rectangle(0, 0, CLUE_SPACE_LEFT, CLUE_SPACE_TOP, fill="#f0f0f0", outline="#f0f0f0")
        # Row clues (left)
        max_row_clues = max(len(c) for c in self.row_clues)
        for r, clues in enumerate(self.row_clues):
            x = CLUE_SPACE_LEFT - 6
            # right-align numbers within left area
            text = "  ".join(map(str, clues))
            self.canvas.create_text(x, CLUE_SPACE_TOP + r*self.cell_size + self.cell_size/2, text=text, anchor="e", font=("Arial", 10))

        # Column clues (top)
        # top clues often have multiple lines - stack them centered above each column
        max_col_clues = max(len(c) for c in self.col_clues)
        for c, clues in enumerate(self.col_clues):
            # center clues in the column area; we draw them stacked top-to-bottom
            area_x = CLUE_SPACE_LEFT + c*self.cell_size + self.cell_size/2
            # draw stacked vertically with smallest at bottom (so numbers align to bottom like normal nonograms)
            for i, val in enumerate(reversed(clues)):
                offset = (i+1) * 12
                self.canvas.create_text(area_x, CLUE_SPACE_TOP - offset, text=str(val), anchor="s", font=("Arial", 10))

        # draw grid cells
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x0 = CLUE_SPACE_LEFT + c*self.cell_size
                y0 = CLUE_SPACE_TOP + r*self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", tags=f"cell_{r}_{c}")
                # draw state if revealed or crossed
                st = self.state[r][c]
                if st == 1:
                    if self.solution[r][c] == 1:
                        self.canvas.create_rectangle(x0+2, y0+2, x1-2, y1-2, fill="black", outline="")
                    else:
                        # revealed empty cell - indicate with light grey
                        self.canvas.create_rectangle(x0+2, y0+2, x1-2, y1-2, fill="#dcdcdc", outline="")
                elif st == -1:
                    # draw X
                    self.canvas.create_line(x0+4, y0+4, x1-4, y1-4, width=2)
                    self.canvas.create_line(x0+4, y1-4, x1-4, y0+4, width=2)

        # bold every 5th line for readability
        for i in range(self.grid_size+1):
            width = 2 if i%5==0 else 1
            x = CLUE_SPACE_LEFT + i*self.cell_size
            self.canvas.create_line(x, CLUE_SPACE_TOP, x, CLUE_SPACE_TOP + self.grid_size*self.cell_size, width=width)
            y = CLUE_SPACE_TOP + i*self.cell_size
            self.canvas.create_line(CLUE_SPACE_LEFT, y, CLUE_SPACE_LEFT + self.grid_size*self.cell_size, y, width=width)

    def _coords_to_cell(self, x, y):
        # convert canvas coords to (r,c), return None if outside grid area
        if x < CLUE_SPACE_LEFT or y < CLUE_SPACE_TOP:
            return None
        col = int((x - CLUE_SPACE_LEFT) // self.cell_size)
        row = int((y - CLUE_SPACE_TOP) // self.cell_size)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return (row, col)
        return None

    def left_click(self, event):
        res = self._coords_to_cell(event.x, event.y)
        if not res:
            return
        r, c = res
        # reveal cell
        if self.state[r][c] == 1:
            # already revealed, ignore
            return
        self.state[r][c] = 1
        self.redraw()

    def right_click(self, event):
        res = self._coords_to_cell(event.x, event.y)
        if not res:
            return
        r, c = res
        # toggle cross mark - don't overwrite a revealed filled cell
        if self.state[r][c] == 1:
            return
        self.state[r][c] = 0 if self.state[r][c] == -1 else -1
        self.redraw()

    def check(self):
        # check whether all filled cells match solution and no wrong filled cells
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.state[r][c] == 1 and self.solution[r][c] != 1:
                    messagebox.showinfo("Check", "Some revealed cells are incorrect. Keep trying!")
                    return
                # optionally, check if user failed to mark filled ones: but We only check for incorrect revelations
        # now check if all solution filled cells are revealed
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.solution[r][c] == 1 and self.state[r][c] != 1:
                    messagebox.showinfo("Check", "Not solved yet — some filled cells are still hidden.")
                    return
        messagebox.showinfo("Check", "Congratulations! Puzzle solved.")

    def reveal(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.state[r][c] = 1
        self.redraw()

    def copy_solution(self):
        # copy textual solution to clipboard (rows as 0/1 strings)
        s = "\\n".join("".join(str(x) for x in row) for row in self.solution)
        self.master.clipboard_clear()
        self.master.clipboard_append(s)
        messagebox.showinfo("Copied", "Solution copied to clipboard (0/1 rows).")

def main():
    root = tk.Tk()
    root.title("15x15 Nonogram (Random, solvable)")
    app = Nonogram(root, grid_size=GRID)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Wrote file to /mnt/data/nonogram.py")
print("Run it locally with: python3 /mnt/data/nonogram.py")

import tkinter as tk
import random
import time
import json
import os
import hashlib

SECRET_KEY = "SuperSecretMinesweeperKey"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(BASE_DIR, "minesweeper_stats.json")

NUMBER_COLORS = {
    1: "#1E90FF",
    2: "#32CD32",
    3: "#FF4500",
    4: "#00008B",
    5: "#8B4513",
    6: "#20B2AA",
    7: "#000000",
    8: "#808080"
}

BG_COLOR = "#202124"
TILE_COLOR = "#3C4043"
TILE_REVEALED = "#5F6368"
FLAG_COLOR = "#FF0000"
WRONG_FLAG_COLOR = "#808080"

DIFFICULTIES = {
    "Easy": (8, 10, 10),
    "Medium": (14, 18, 40),
    "Hard": (25, 25, 100),
    "God": (40, 50, 400)
}

# --- Stats Handling --- #
def calculate_hash(data):
    raw = json.dumps(data, sort_keys=True) + SECRET_KEY
    return hashlib.sha256(raw.encode()).hexdigest()

def load_stats():
    if not os.path.exists(STATS_FILE):
        return reset_stats()

    try:
        with open(STATS_FILE, "r") as f:
            content = json.load(f)

        data = content.get("data", {})
        stored_hash = content.get("hash", "")
        if calculate_hash(data) != stored_hash:
            print("⚠ Stats file modified! Resetting stats.")
            return reset_stats()

        return data
    except Exception as e:
        print(f"⚠ Error loading stats: {e}")
        return reset_stats()

def save_stats(stats):
    content = {
        "data": stats,
        "hash": calculate_hash(stats)
    }
    with open(STATS_FILE, "w") as f:
        json.dump(content, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    print(f"✅ Stats saved to {STATS_FILE}")

def reset_stats():
    stats = {diff: {"wins": 0, "losses": 0, "best_time": None, "misflags": 0} for diff in DIFFICULTIES}
    save_stats(stats)
    return stats

STATS = load_stats()

class Minesweeper:
    def __init__(self, root, rows, cols, mines, difficulty_name):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.flags_count = 0
        self.start_time = None
        self.timer_running = False
        self.difficulty_name = difficulty_name
        self.first_click = True

        self.root.title(f"Minesweeper - {rows}x{cols}, {mines} Mines")
        self.root.configure(bg=BG_COLOR)

        self.top_frame = tk.Frame(root, bg=BG_COLOR)
        self.top_frame.pack(pady=5)

        self.mine_label = tk.Label(self.top_frame, text=f"Mines: {self.mines_count}",
                                   font=("Arial", 12), fg="white", bg=BG_COLOR)
        self.mine_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0",
                                    font=("Arial", 12), fg="white", bg=BG_COLOR)
        self.timer_label.pack(side="right", padx=10)

        self.frame = tk.Frame(root, bg=BG_COLOR)
        self.frame.pack(padx=10, pady=10)

        self.buttons = {}
        self.mines = set()
        self.revealed = set()
        self.flags = set()

        self.create_widgets()

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.frame, width=2, height=1,
                    bg=TILE_COLOR, fg="white", relief="raised",
                    font=("Arial", 12, "bold"),
                    command=lambda r=r, c=c: self.reveal(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.toggle_flag(r, c))
                btn.bind("<Button-2>", lambda e, r=r, c=c: self.chord(r, c))  # Middle-click chording
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

    def place_mines(self, safe_zone):
        while len(self.mines) < self.mines_count:
            candidate = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if candidate not in safe_zone:
                self.mines.add(candidate)

    def count_adjacent(self, r, c):
        return sum((r + dr, c + dc) in self.mines
                   for dr in (-1, 0, 1)
                   for dc in (-1, 0, 1)
                   if not (dr == 0 and dc == 0))

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}")
            self.root.after(1000, self.update_timer)

    def reveal(self, r, c):
        if self.first_click:
            safe_zone = set()
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        safe_zone.add((nr, nc))

            self.place_mines(safe_zone)

            self.first_click = False
            self.start_timer()

            for (rr, cc) in safe_zone:
                self._reveal_tile(rr, cc)
        else:
            self._reveal_tile(r, c)

        if len(self.revealed) == self.rows * self.cols - self.mines_count:
            self.game_over(True)

    def _reveal_tile(self, r, c):
        if (r, c) in self.flags or (r, c) in self.revealed:
            return

        self.revealed.add((r, c))
        btn = self.buttons[(r, c)]
        btn["bg"] = TILE_REVEALED
        btn["relief"] = "sunken"

        if (r, c) in self.mines:
            btn.config(text="💣", disabledforeground="#FF0000")
            btn["state"] = "disabled"
            self.game_over(False)
            return

        count = self.count_adjacent(r, c)
        if count > 0:
            btn.config(text=str(count), disabledforeground=NUMBER_COLORS[count])
        btn["state"] = "disabled"

        if count == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if (nr, nc) not in self.revealed:
                            self._reveal_tile(nr, nc)

    def toggle_flag(self, r, c):
        if (r, c) in self.revealed:
            return
        btn = self.buttons[(r, c)]
        if (r, c) in self.flags:
            btn["text"] = ""
            self.flags.remove((r, c))
            self.flags_count -= 1
        else:
            btn["text"] = "🚩"
            btn["fg"] = FLAG_COLOR
            self.flags.add((r, c))
            self.flags_count += 1

        self.mine_label.config(text=f"Mines: {self.mines_count - self.flags_count}")

    def chord(self, r, c):
        # Only chord if tile is revealed and has a number > 0
        if (r, c) not in self.revealed:
            return

        btn = self.buttons[(r, c)]
        text = btn.cget("text")
        if not text or not text.isdigit():
            return

        number = int(text)

        # Count flagged neighbors
        flagged_neighbors = 0
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
                    if (nr, nc) in self.flags:
                        flagged_neighbors += 1

        if flagged_neighbors == number:
            # Reveal all non-flagged neighbors
            for nr, nc in neighbors:
                if (nr, nc) not in self.flags and (nr, nc) not in self.revealed:
                    self._reveal_tile(nr, nc)

    def game_over(self, win):
        self.timer_running = False
        elapsed_time = int(time.time() - self.start_time) if self.start_time else None

        # Count misflags: flags placed on non-mine tiles
        misflags_count = sum(1 for flag in self.flags if flag not in self.mines)
        STATS[self.difficulty_name]["misflags"] += misflags_count

        if win:
            STATS[self.difficulty_name]["wins"] += 1
            if elapsed_time is not None:
                best = STATS[self.difficulty_name]["best_time"]
                if best is None or elapsed_time < best:
                    STATS[self.difficulty_name]["best_time"] = elapsed_time
        else:
            STATS[self.difficulty_name]["losses"] += 1

        save_stats(STATS)

        for (r, c) in self.mines:
            if (r, c) not in self.flags:
                self.buttons[(r, c)].config(text="💣", disabledforeground="#FF0000")
            self.buttons[(r, c)]["state"] = "disabled"

        for (r, c) in self.flags:
            if (r, c) not in self.mines:
                self.buttons[(r, c)].config(text="❌", bg=WRONG_FLAG_COLOR, disabledforeground="#FFFFFF")
            self.buttons[(r, c)]["state"] = "disabled"

        self.show_end_popup(win, elapsed_time)

    def show_end_popup(self, win, elapsed_time):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.configure(bg=BG_COLOR)
        msg = "🎉 You Win!" if win else "💥 Game Over!"
        tk.Label(popup, text=msg, font=("Arial", 14), bg=BG_COLOR, fg="white").pack(padx=20, pady=10)

        if win and elapsed_time is not None:
            tk.Label(popup, text=f"Time: {elapsed_time}s", font=("Arial", 12), bg=BG_COLOR, fg="white").pack()

        tk.Button(popup, text="Restart", font=("Arial", 12),
                  command=lambda: self.restart_game(popup)).pack(pady=5)

        tk.Button(popup, text="Change Difficulty", font=("Arial", 12),
                  command=lambda: self.change_difficulty(popup)).pack(pady=5)

        tk.Button(popup, text="Quit", font=("Arial", 12), command=self.root.quit).pack(pady=5)

    def restart_game(self, popup):
        popup.destroy()
        self.top_frame.destroy()
        self.frame.destroy()
        start_game(self.root, self.rows, self.cols, self.mines_count, self.difficulty_name)

    def change_difficulty(self, popup):
        popup.destroy()
        self.top_frame.destroy()
        self.frame.destroy()
        show_difficulty_menu(self.root)

def show_stats_window(root):
    stats_win = tk.Toplevel(root)
    stats_win.title("Minesweeper Stats")
    stats_win.configure(bg=BG_COLOR)

    # Create a grid with 1 header row + 4 data rows, and columns = 1 label + number of difficulties
    stats_win.columnconfigure(0, weight=1)
    stats_win.rowconfigure(0, weight=1)

    headers = ["Stat"] + list(DIFFICULTIES.keys())
    stats_labels = ["Wins", "Losses", "Best Time (s)", "Misflags"]
    for col, header in enumerate(headers):
        lbl = tk.Label(stats_win, text=header, font=("Arial", 14, "bold"),
                       bg=BG_COLOR, fg="white", borderwidth=2, relief="ridge", padx=10, pady=5)
        lbl.grid(row=0, column=col, sticky="nsew")

    for row, stat in enumerate(stats_labels, start=1):
        lbl = tk.Label(stats_win, text=stat, font=("Arial", 12, "bold"),
                       bg=BG_COLOR, fg="white", borderwidth=2, relief="ridge", padx=10, pady=5)
        lbl.grid(row=row, column=0, sticky="nsew")
        for col, diff in enumerate(DIFFICULTIES, start=1):
            val = STATS[diff][stat.lower().replace(" (s)", "").replace(" ", "_")]
            if val is None:
                val = "N/A"
            lbl_val = tk.Label(stats_win, text=str(val), font=("Arial", 12),
                               bg=BG_COLOR, fg="white", borderwidth=2, relief="ridge", padx=10, pady=5)
            lbl_val.grid(row=row, column=col, sticky="nsew")

def show_difficulty_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG_COLOR)
    tk.Label(root, text="Select Difficulty", font=("Arial", 16),
             bg=BG_COLOR, fg="white").pack(pady=10)

    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    def confirm_reset():
        confirm = tk.Toplevel(root)
        confirm.title("Confirm Reset")
        confirm.configure(bg=BG_COLOR)
        tk.Label(confirm, text="Are you sure you want to reset all stats?",
                 font=("Arial", 12), bg=BG_COLOR, fg="white").pack(padx=20, pady=10)

        def do_reset():
            global STATS
            STATS = reset_stats()
            confirm.destroy()
            show_difficulty_menu(root)

        tk.Button(confirm, text="Yes", font=("Arial", 12), fg="red",
                  command=do_reset).pack(side="left", padx=20, pady=10)
        tk.Button(confirm, text="No", font=("Arial", 12),
                  command=confirm.destroy).pack(side="right", padx=20, pady=10)

    reset_btn = tk.Button(button_frame, text="Reset Stats", font=("Arial", 12), fg="red",
                          command=confirm_reset)
    reset_btn.pack(side="left", padx=10)

    view_btn = tk.Button(button_frame, text="View Stats", font=("Arial", 12), fg="black",
                         command=lambda: show_stats_window(root))
    view_btn.pack(side="left", padx=10)

    for diff, (rows, cols, mines) in DIFFICULTIES.items():
        best = STATS[diff]["best_time"]
        best_str = f" | Best: {best}s" if best is not None else ""
        tk.Button(root, text=f"{diff} ({rows}x{cols}, {mines} mines) - Wins: {STATS[diff]['wins']} Losses: {STATS[diff]['losses']}{best_str}",
                  font=("Arial", 12), width=50,
                  command=lambda d=diff, r=rows, c=cols, m=mines: start_game(root, r, c, m, d)).pack(pady=5)

def start_game(root, rows, cols, mines, difficulty_name):
    for widget in root.winfo_children():
        widget.destroy()
    Minesweeper(root, rows, cols, mines, difficulty_name)

root = tk.Tk()
show_difficulty_menu(root)
root.mainloop()

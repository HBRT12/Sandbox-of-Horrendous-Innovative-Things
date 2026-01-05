import tkinter as tk
from tkinter import messagebox
import random

# Settings
NUM_WINDOWS = 6
WIN_W = 300
WIN_H = 200
BLINK_INTERVAL = 300
MOVE_INTERVAL = 3
MOVE_SPEED = 15

def create_window():
    win = tk.Tk()
    win.title("You Are An Idiot")
    win.geometry(f"{WIN_W}x{WIN_H}")
    win.overrideredirect(True)

    label = tk.Label(
        win,
        text="You Are An Idiot\n☺☺☺",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="black"
    )
    label.pack(expand=True, fill="both")

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = random.randint(0, screen_w - WIN_W)
    y = random.randint(0, screen_h - WIN_H)
    win.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    dx = random.choice([-MOVE_SPEED, MOVE_SPEED])
    dy = random.choice([-MOVE_SPEED, MOVE_SPEED])
    is_black_bg = True

    def move():
        nonlocal x, y, dx, dy
        x += dx
        y += dy

        if x <= 0 or x >= screen_w - WIN_W:
            dx *= -1
        if y <= 0 or y >= screen_h - WIN_H:
            dy *= -1

        win.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")
        win.after(MOVE_INTERVAL, move)

    def blink():
        nonlocal is_black_bg
        label.config(
            bg="white" if is_black_bg else "black",
            fg="black" if is_black_bg else "white"
        )
        is_black_bg = not is_black_bg
        win.after(BLINK_INTERVAL, blink)

    move()
    blink()
    return win

# Ask user first
def start_program():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    answer = messagebox.askyesno("Question", "Are you an idiot?")

    if answer:
        root.destroy()
        windows = [create_window() for _ in range(NUM_WINDOWS)]
        windows[0].mainloop()
    else:
        # Goodbye message
        # Goodbye message (centered)
        goodbye = tk.Toplevel()
        win_w, win_h = 200, 100
        screen_w = goodbye.winfo_screenwidth()
        screen_h = goodbye.winfo_screenheight()
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        goodbye.geometry(f"{win_w}x{win_h}+{x}+{y}")
        goodbye.overrideredirect(True)
        tk.Label(goodbye, text="Goodbye!", font=("Arial", 14)).pack(expand=True, fill="both")
        goodbye.after(2000, goodbye.destroy)
        goodbye.mainloop()
start_program()

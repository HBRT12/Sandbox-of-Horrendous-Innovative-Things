import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import json
import os
import sys
import ctypes
import hashlib

# DPI Awareness for Windows
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

CARD_VALUES = {1: '01', 11: '11', 12: '12', 13: '13'}
SUITS = ['c', 'd', 'h', 's']
SAVE_FOLDER = "saves"
NUM_SLOTS = 3
CARD_IMAGES = {}

# ====================== Load/Save ======================

def load_card_images():
    for suit in SUITS:
        for rank in list(CARD_VALUES.keys()) + list(range(2, 11)):
            label = CARD_VALUES.get(rank, f"{rank:02d}")
            file_name = f"cards/{label}{suit}.gif"
            try:
                image = tk.PhotoImage(file=file_name)
                CARD_IMAGES[f"{label}{suit}".lower()] = image
            except Exception as e:
                print(f"Missing or invalid file: {file_name} ({e})")
    CARD_IMAGES["BACK"] = tk.PhotoImage(file="cards/back01.gif")

def get_save_path(slot):
    return os.path.join(SAVE_FOLDER, f"save{slot}.json")

def compute_hash(data_dict):
    data_copy = data_dict.copy()
    data_copy.pop("hash", None)
    json_str = json.dumps(data_copy, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()

def load_save(slot):
    path = get_save_path(slot)
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                data = json.load(f)
                saved_hash = data.get("hash", "")
                calc_hash = compute_hash(data)
                if saved_hash != calc_hash:
                    raise ValueError("Save file hash mismatch! Data may be corrupted or tampered.")
                return data
            except Exception as e:
                print(f"Load error for save slot {slot}: {e}")
    data = {"wins": 0, "losses": 0, "draws": 0, "name": f"Save Slot {slot+1}"}
    data["hash"] = compute_hash(data)
    save_save(slot, data)
    return data

def save_save(slot, data):
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    data["hash"] = compute_hash(data)
    with open(get_save_path(slot), 'w') as f:
        json.dump(data, f)

def delete_save(slot):
    path = get_save_path(slot)
    if os.path.exists(path):
        os.remove(path)

# ====================== Save Slot UI ======================

def choose_save_slot():
    def load_slot(slot):
        nonlocal selected_slot
        selected_slot = slot
        save_window.destroy()

    def delete_slot(slot):
        if messagebox.askyesno("Confirm Delete", f"Delete Save Slot {slot + 1}?"):
            delete_save(slot)
            refresh()

    def rename_slot(slot):
        new_name = simpledialog.askstring("Rename Save", "Enter new save name:")
        if new_name:
            data = load_save(slot)
            data['name'] = new_name
            save_save(slot, data)
            refresh()

    def refresh():
        for widget in save_window.winfo_children():
            widget.destroy()
        tk.Label(save_window, text="Choose Save Slot:", font=("Arial", 14)).pack(pady=5)
        for i in range(NUM_SLOTS):
            data = load_save(i)
            frame = tk.Frame(save_window)
            frame.pack(pady=5)
            label = f"[{i+1}] {data['name']} — W:{data['wins']} L:{data['losses']} D:{data['draws']}"
            tk.Label(frame, text=label).pack(side="left")
            tk.Button(frame, text="Load", command=lambda i=i: load_slot(i)).pack(side="left", padx=5)
            tk.Button(frame, text="Rename", command=lambda i=i: rename_slot(i)).pack(side="left", padx=5)
            tk.Button(frame, text="Delete", command=lambda i=i: delete_slot(i)).pack(side="left", padx=5)

    selected_slot = None
    save_window = tk.Toplevel(root)
    save_window.title("Save Slots")
    save_window.grab_set()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_w = root.winfo_width()
    root_h = root.winfo_height()
    save_window.geometry(f"+{root_x}+{root_y + root_h + 10}")

    refresh()
    root.wait_window(save_window)
    return selected_slot

# ====================== Game Logic ======================

def deal_card():
    rank = random.choice(list(CARD_VALUES.keys()) + list(range(2, 11)))
    suit = random.choice(SUITS)
    return (rank, suit)

def card_key(card):
    # card can be (rank, suit) or (rank, suit, value) for ace
    rank = card[0]
    suit = card[1]
    label = CARD_VALUES.get(rank, f"{rank:02d}")
    return f"{label}{suit}"

def calculate_score(hand):
    score = 0
    for card in hand:
        rank = card[0]
        # if card has a chosen value (ace), use that
        if len(card) == 3:
            value = card[2]
        else:
            if rank == 1:
                value = 11  # default ace value for dealer or if no choice
            elif rank in [11, 12, 13]:
                value = 10
            else:
                value = rank
        score += value
    return score

def update_ui():
    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in dealer_frame.winfo_children():
        widget.destroy()

    for card in player_hand:
        label = tk.Label(player_frame, image=CARD_IMAGES[card_key(card).lower()])
        label.pack(side="left")

    if game_over:
        # Show all dealer cards
        for card in dealer_hand:
            label = tk.Label(dealer_frame, image=CARD_IMAGES[card_key(card).lower()])
            label.pack(side="left")
    else:
        # Show only first dealer card + back cards
        if dealer_hand:
            label = tk.Label(dealer_frame, image=CARD_IMAGES[card_key(dealer_hand[0]).lower()])
            label.pack(side="left")
            for _ in dealer_hand[1:]:
                tk.Label(dealer_frame, image=CARD_IMAGES["BACK"]).pack(side="left")

    player_score = calculate_score(player_hand)
    player_label.config(text=f"Player's Hand - Score: {player_score}")
    dealer_label.config(text="Dealer's Hand:")
    stats_label.config(text=f"[{save_slot + 1}] {current_save['name']}  Wins: {current_save['wins']}  Losses: {current_save['losses']}  Draws: {current_save['draws']}")

def check_winner():
    global game_over
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > 21:
        result = "Bust! You lose."
        current_save['losses'] += 1
    elif dealer_score > 21 or player_score > dealer_score:
        result = "You win!"
        current_save['wins'] += 1
    elif player_score < dealer_score:
        result = "You lose."
        current_save['losses'] += 1
    else:
        result = "Draw."
        current_save['draws'] += 1

    game_over = True
    save_save(save_slot, current_save)
    result_label.config(text=result)
    update_ui()

def choose_ace_value(suit, callback):
    def set_value(val):
        popup.destroy()
        callback(val)

    popup = tk.Toplevel(root)
    popup.title("Ace Drawn!")
    popup.grab_set()

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_w = root.winfo_width()
    popup.geometry(f"+{root_x + root_w//2}+{max(0, root_y - 100)}")

    tk.Label(popup, text="Choose value for Ace:", font=("Arial", 12)).pack(pady=5)
    tk.Button(popup, text="1", width=10, command=lambda: set_value(1)).pack(pady=5)
    tk.Button(popup, text="11", width=10, command=lambda: set_value(11)).pack(pady=5)

def deal_initial_player_card(count, on_done):
    if count == 0:
        on_done()
        return

    rank, suit = deal_card()
    if rank == 1:
        def after_choice(val):
            # store ace with chosen value
            player_hand.append((1, suit, val))
            deal_initial_player_card(count - 1, on_done)
        choose_ace_value(suit, after_choice)
    else:
        player_hand.append((rank, suit))
        deal_initial_player_card(count - 1, on_done)

def hit():
    if not game_over:
        rank, suit = deal_card()
        if rank == 1:
            def ace_choice(val):
                player_hand.append((1, suit, val))
                update_ui()
                if calculate_score(player_hand) > 21:
                    check_winner()
            choose_ace_value(suit, ace_choice)
        else:
            player_hand.append((rank, suit))
            update_ui()
            if calculate_score(player_hand) > 21:
                check_winner()

def stand():
    global game_over
    if not game_over:
        while calculate_score(dealer_hand) < 17:
            rank, suit = deal_card()
            if rank == 1:
                # dealer uses 11 if no bust else 1
                if calculate_score(dealer_hand) + 11 <= 21:
                    dealer_hand.append((1, suit, 11))
                else:
                    dealer_hand.append((1, suit, 1))
            else:
                dealer_hand.append((rank, suit))
        check_winner()

def reset_game():
    global player_hand, dealer_hand, game_over
    game_over = False  # reset before dealing cards

    player_hand = []
    dealer_hand = []

    def after_player():
        for _ in range(2):
            rank, suit = deal_card()
            if rank == 1:
                # dealer default ace is 11 if no bust else 1
                if calculate_score(dealer_hand) + 11 <= 21:
                    dealer_hand.append((1, suit, 11))
                else:
                    dealer_hand.append((1, suit, 1))
            else:
                dealer_hand.append((rank, suit))
        update_ui()

    deal_initial_player_card(2, after_player)

    result_label.config(text="")
    enable_buttons()

def show_card_values():
    popup = tk.Toplevel(root)
    popup.title("Card Values")
    popup.grab_set()

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_w = root.winfo_width()
    popup.geometry(f"+{root_x + root_w + 10}+{root_y}")

    tk.Label(popup, text="Card Values (J, Q, K = 10):", font=("Arial", 12)).pack(pady=5)
    for rank in [1] + list(range(2, 11)) + [11, 12, 13]:
        name = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}.get(rank, str(rank))
        value = 10 if rank in [11, 12, 13] else (11 if rank == 1 else rank)
        tk.Label(popup, text=f"{name}: {value}").pack()

def disable_buttons():
    for widget in button_frame.winfo_children():
        widget.config(state="disabled")

def enable_buttons():
    for widget in button_frame.winfo_children():
        widget.config(state="normal")

# ====================== Main ======================

root = tk.Tk()
root.title("Blackjack")

load_card_images()

player_hand = []
dealer_hand = []
game_over = False

save_slot = choose_save_slot()
if save_slot is None:
    save_slot = 0
current_save = load_save(save_slot)

# UI Setup

top_frame = tk.Frame(root)
top_frame.pack(pady=5)

stats_label = tk.Label(top_frame, text="")
stats_label.pack()

player_label = tk.Label(root, text="Player's Hand")
player_label.pack()
player_frame = tk.Frame(root)
player_frame.pack()

dealer_label = tk.Label(root, text="Dealer's Hand")
dealer_label.pack()
dealer_frame = tk.Frame(root)
dealer_frame.pack()

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Hit", command=hit).pack(side="left", padx=10)
tk.Button(button_frame, text="Stand", command=stand).pack(side="left", padx=10)
tk.Button(button_frame, text="Reset", command=reset_game).pack(side="left", padx=10)
tk.Button(button_frame, text="Card Values", command=show_card_values).pack(side="left", padx=10)

reset_game()
root.mainloop()

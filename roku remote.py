import tkinter as tk
from roku import Roku

roku = Roku("192.168.0.20")

root = tk.Tk()
root.geometry('300x150')
root.title('Roku Remote')
root.focus_set()  # So key events are captured

def on_key(event):
    key = event.keysym
    print(f"Pressed: {key}")  # Debugging line, optional

    if key == 'Up':
        roku.up()
    elif key == 'Down':
        roku.down()
    elif key == 'Left':
        roku.left()
    elif key == 'Right':
        roku.right()
    elif key == 'Return':  # 'Return' is Enter key
        roku.select()
    elif key == 'BackSpace':
        roku.back()
    elif key == 'Shift_R':
        roku.home()
    elif key == 'Space':
        roku.play()

root.bind('<KeyPress>', on_key)

root.mainloop()

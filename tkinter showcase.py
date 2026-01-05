import tkinter as tk          # Import Tkinter and give it the alias 'tk'
from tkinter import messagebox  # Import messagebox to show popup messages

# ---------------- Helper Function ---------------- #
def show_value(value):
    """
    Show a popup message with the current value of a widget.
    value: The value to display (string, number, boolean, etc.)
    """
    messagebox.showinfo("Widget Value", str(value))  # Show info dialog with value

# ---------------- Root Window ---------------- #
root = tk.Tk()                     # Create the main application window
root.title("Root Window")          # Set the title of the main window
root.geometry("600x400")           # Set width and height of the window
root.configure(bg="lightblue")     # Set background color of root window

# ---------------- Label in Root ---------------- #
root_label = tk.Label(             # Create a Label widget
    root,                          # Parent is root window
    text="This is a Label",        # The text displayed on the label
    bg="lightblue",                # Background color of the label
    fg="black",                     # Text color
    font=("Arial", 14),             # Font family and size
    width=20,                       # Width in characters
    height=2,                       # Height in lines
    relief="solid",                 # Border style: solid, raised, sunken, etc.
    anchor="center"                 # Text alignment within the label
)
root_label.pack(pady=10)           # Pack the label into the window with vertical padding

# Button to show label value
tk.Button(
    root,
    text="Get Label Value",         # Text shown on button
    command=lambda: show_value(root_label.cget("text"))  # Show label text on click
).pack()

# ---------------- Entry in Root ---------------- #
entry_var = tk.StringVar(value="Default text")  # StringVar to store Entry value

root_entry = tk.Entry(              # Create Entry widget
    root,                           # Parent is root
    textvariable=entry_var,         # Link Entry to variable
    bg="white",                     # Background color
    fg="black",                     # Text color
    font=("Arial", 12),             # Font style
    width=30,                       # Width in characters
    justify="left",                 # Text alignment inside box
    relief="sunken"                 # Border style
)
root_entry.pack(pady=10)            # Pack Entry with padding

# Button to get Entry value
tk.Button(
    root,
    text="Get Entry Value",          # Button text
    command=lambda: show_value(entry_var.get())  # Show Entry content
).pack()

# ---------------- Button in Root ---------------- #
def on_button_click():               # Function to execute when button clicked
    show_value("Button was clicked!")  # Show popup with a message

root_button = tk.Button(             # Create Button widget
    root,                            # Parent is root window
    text="Click Me",                  # Text on button
    command=on_button_click,          # Function called when button clicked
    bg="green",                       # Background color
    fg="white",                       # Text color
    font=("Arial", 12),               # Font style
    width=15,                         # Width in characters
    height=2,                         # Height in rows
    relief="raised",                  # Border style
    cursor="hand2"                    # Cursor style when hovering over button
)
root_button.pack(pady=10)            # Pack button with vertical padding

# ---------------- Function to Open New Window ---------------- #
def open_new_window():               # Function to open a new top-level window
    new_win = tk.Toplevel(root)      # Create a new window (child of root)
    new_win.title("New Window")      # Set title of new window
    new_win.geometry("500x300")      # Set size of new window
    new_win.configure(bg="lightyellow")  # Set background color

    # ---------------- Label in New Window ---------------- #
    new_label = tk.Label(             # Create a Label inside new window
        new_win,                      # Parent is new_win
        text="New Window Label",       # Text displayed
        bg="lightyellow",             # Background color
        fg="black",                    # Text color
        font=("Arial", 14),            # Font style
        width=25,                       # Width in characters
        height=2,                       # Height in lines
        relief="ridge",                 # Border style
        anchor="center"                 # Text alignment
    )
    new_label.pack(pady=10)           # Pack label with padding

    # Button to get label value
    tk.Button(
        new_win,
        text="Get Label Value",        # Button text
        command=lambda: show_value(new_label.cget("text"))  # Show label content
    ).pack()

    # ---------------- Checkbutton in New Window ---------------- #
    check_var = tk.BooleanVar(value=False)  # Variable to track checkbutton
    new_check = tk.Checkbutton(
        new_win,                        # Parent window
        text="Check Me",                # Text next to checkbox
        variable=check_var,             # Linked variable
        onvalue=True,                   # Value when checked
        offvalue=False,                 # Value when unchecked
        font=("Arial", 12),             # Font style
        bg="white",                     # Background color
        fg="black",                     # Text color
        relief="flat",                  # Border style
        anchor="w"                      # Text alignment
    )
    new_check.pack(pady=10)            # Pack checkbox

    # Button to get Checkbutton value
    tk.Button(
        new_win,
        text="Get Checkbutton Value",  # Button text
        command=lambda: show_value(check_var.get())  # Show True/False
    ).pack()

    # ---------------- Radiobuttons in New Window ---------------- #
    radio_var = tk.StringVar(value="Option 1")  # Variable to track selected radio
    tk.Radiobutton(
        new_win,
        text="Option 1",                # Option text
        variable=radio_var,             # Linked variable
        value="Option 1"                # Value when selected
    ).pack(anchor="center")
    tk.Radiobutton(
        new_win,
        text="Option 2",                # Option text
        variable=radio_var,             # Linked variable
        value="Option 2"                # Value when selected
    ).pack(anchor="center")

    # Button to get Radiobutton value
    tk.Button(
        new_win,
        text="Get Radio Value",         # Button text
        command=lambda: show_value(radio_var.get())  # Show selected option
    ).pack()

# ---------------- Button on Root to Open New Window ---------------- #
tk.Button(
    root,
    text="Open New Window",             # Button text
    command=open_new_window             # Function to open new window
).pack(pady=20)

# ---------------- Run Mainloop ---------------- #
root.mainloop()  # Start Tkinter event loop 

import tkinter as tk
import tkinter.messagebox as messagebox
import sys
create_pin_1 = [] # Stores PIN made on creation screen
create_pin_2 = [] # Stores PIN made on confirmation screen
lock_screen_code = [] # Stores PIN entered on lock screen
code_from_file = [] # Stores the PIN from the pin.txt file with each number as a list element
confirming = 'En' # Pin entry status: Creating, Confirming, Entering
unlock_attempts = 0
pinfile = open('pin.TXT','r')
for line in pinfile:
    filecode=line
pinfile.close()

for each in filecode:
    code_from_file.append(each)
    
def window_closed(window): # Function shows root window again once chosen window is closed
    window.destroy()
    root.deiconify()

def update_pin_display(length_1,length_2,length_3):
    if confirming == 'Cr':
        pin_display.config(text='Create your PIN:\n'+'*'*length_1)
    elif confirming == 'Co':
        pin_display.config(text='Re-enter your PIN:\n'+'*'*length_2)
    elif confirming == 'En':
        try:
            pin_window.title('Enter PIN')
            pin_display.config(text='Enter your PIN:\n'+'*'*length_3)
        except:
            pass
def type_number(num):
    if confirming == 'Cr':
        if not len(create_pin_1) >= 6:
            create_pin_1.append(num)
        else:
            messagebox.showinfo('Max length!','The PIN can only be a max of 6 digits.')
    elif confirming == 'Co':
        if not len(create_pin_2) >= 6:
            create_pin_2.append(num)
        else:
            messagebox.showinfo('Max length!','The PIN can only be a max of 6 digits.')
    elif confirming == 'En':
            lock_screen_code.append(num)
    update_pin_display(len(create_pin_1),len(create_pin_2),len(lock_screen_code))

def backspace():
    try:
        if confirming == 'Cr':
            create_pin_1.pop(-1)
        elif confirming == 'Co':
            create_pin_2.pop(-1)
        elif confirming == 'En':
            lock_screen_code.pop(-1)
    except:
        pass
    update_pin_display(len(create_pin_1),len(create_pin_2),len(lock_screen_code))

def enter():
    global unlock_attempts
    global lock_screen_code
    if confirming == 'Cr':
        if len(create_pin_1) <= 4:
            messagebox.showerror('Too short!','Your created PIN must be at least 4 characters long.')
    elif confirming == 'Co':
        if create_pin_1 != create_pin_2:
            messagebox.showerror('Not matching!','The 2 PINs do not match. Please try again.')
    elif confirming == 'En':
        if lock_screen_code != code_from_file:
            unlock_attempts += 1
            lock_screen_code = []
            if unlock_attempts < 5:
                messagebox.showwarning('Incorrect PIN!', f'The PIN you have entered is incorrect. You have {5-unlock_attempts} attempts left')
            else:
                pin_window.destroy()
                messagebox.showerror('Incorrect PIN!','You have run out of password attempts. The program will now close')
                sys.exit()
        elif lock_screen_code == code_from_file:
            messagebox.showinfo('Access granted!','You entered the correct PIN, welcome back.')
            pin_window.destroy()
            root.deiconify()
    update_pin_display(len(create_pin_1),len(create_pin_2),len(lock_screen_code))
def create_pin_window():
    root.withdraw()# Hides root window while pin is being made
    global create_pin_1
    global create_pin_2
    create_pin_1 = []
    create_pin_2 = []
    global pin_window
    pin_window = tk.Toplevel(root)
    pin_window.title('Create PIN')
    pin_window.geometry('300x600')
    button_1=tk.Button(pin_window,
                       text='1',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('1'))
    button_2=tk.Button(pin_window,
                       text='2',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('2'))
    button_3=tk.Button(pin_window,
                       text='3',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('3'))
    button_4=tk.Button(pin_window,
                       text='4',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('4'))
    button_5=tk.Button(pin_window,
                       text='5',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('5'))
    button_6=tk.Button(pin_window,
                       text='6',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('6'))
    button_7=tk.Button(pin_window,
                       text='7',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('7'))
    button_8=tk.Button(pin_window,
                       text='8',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('8'))
    button_9=tk.Button(pin_window,
                       text='9',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('9'))
    button_0=tk.Button(pin_window,
                       text='0',
                       font=('Arial',20),
                       activebackground='gray',
                       command=lambda: type_number('0'))
    button_backspace=tk.Button(pin_window,
                               text='⌫',
                               font=('Arial',20),
                               activebackground='gray',
                               command=backspace)
    button_enter=tk.Button(pin_window,
                           text='Enter',
                           font=('Arial',20),
                           activebackground='gray',
                           command=enter)
    global pin_display
    pin_display=tk.Label(pin_window,
                         text='Create your pin:\n',
                         font=('Arial',14),
                         anchor='center',
                         relief='solid')
    button_1.place(x=0, y=200, height=100, width=100)
    button_2.place(x=100, y=200, height=100, width=100)
    button_3.place(x=200, y=200, height=100, width=100)
    button_4.place(x=0, y=300, height=100, width=100)
    button_5.place(x=100, y=300, height=100, width=100)
    button_6.place(x=200, y=300, height=100, width=100)
    button_7.place(x=0, y=400, height=100, width=100)
    button_8.place(x=100, y=400, height=100, width=100)
    button_9.place(x=200, y=400, height=100, width=100)
    button_0.place(x=100, y=500, height=100, width=100)
    button_backspace.place(x=0, y=500, height=100, width=100)
    pin_display.place(x=50, y=50, height=100, width=200)
    button_enter.place(x=200, y=500, height=100, width=100)
    if confirming in ['Cr','Co']:
        pin_window.protocol('WM_DELETE_WINDOW',lambda: window_closed(pin_window))
    else:
        pin_window.protocol('WM_DELETE_WINDOW',root.destroy)
        
def back_to_main():
    pin_window.destroy()
    root.deiconify()

root=tk.Tk()
root.geometry('400x600')
make_pin_button = tk.Button(root,
                            text=f'Create PIN',
                            command=create_pin_window)
root.withdraw()
make_pin_button.pack()
create_pin_window()
update_pin_display(len(create_pin_1),len(create_pin_2),len(lock_screen_code))
root.mainloop()

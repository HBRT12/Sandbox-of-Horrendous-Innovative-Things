import tkinter as tk

root=tk.Tk()
root.geometry('300x500')
b1=tk.Button(root,
             text='Click me',
             command=lambda: print('Button clicked!'))

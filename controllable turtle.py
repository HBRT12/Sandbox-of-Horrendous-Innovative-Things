from turtle import *
import tkinter as tk
import random

bgcolor("white")
color("black")
setheading(90)
speed("normal")
def f5():
    forward(5)
def f10():
    forward(10)
def f50():
    forward(50)
def b5():
    forward(-5)
def b10():
    forward(-10)
def b50():
    forward(-50)
def pd():
    pendown()
def pu():
    penup()
def resetangle():
    setheading(90)
def l5():
    left(5)
def l10():
    left(10)
def l45():
    left(45)
def r5():
    right(5)
def r10():
    right(10)
def r45():
    right(45)
def bfill():
    begin_fill()
def efill():
    end_fill()
def cls():
    clear()
def crc():
    csize=0
    while True:
        try:
            radius=int(input("How big do you want the circle>>> "))
            break
        except:
            print("ERROR: Expected integer but recieved float/string")
    circle(radius)
def resetpos():
    penup()
    goto(0,0)
    pendown()
def choosetcolor():
    while True:
        try:
            user_color=input("please type the turtle colour you want to use (HEX/named colour)>>>")
            color(user_color)
            break
        except:
            print("ERROR: that is an invalid color")
def choosebgcolor():
    while True:
        try:
            user_color=input("please type the bg colour you want to use (HEX/named colour)>>>")
            bgcolor(user_color)
            break
        except:
            print("ERROR: that is an invalid color")
def resettcolor():
    color("black")
def resetbgcolor():
    bgcolor("white")
def changewidth():
    while True:
        try:
            pwidth=int(input("How wide do you want the pen>>> "))
            width(pwidth)
            break
        except:
            print("ERROR: Invalid width")
def undo_this():
    undo()
def speedchange():
    while True:
        try:
            user_speed=int(input("How fast do you want the turtle to move (0-10)>>> "))
            speed(user_speed)
            break
        except:
            print("I can't set the speed to that!")
def toggle_vis():
    if isvisible():
        hideturtle()
    else:
        showturtle()
root=tk.Tk()
f3=tk.Button(root,
             text="Forward\n50",
             command=f50,
             width=8,
             height=4,
             font=("ariel",10))
f3.grid(row=0, column=3)

f2=tk.Button(root,
             text="Forward\n10",
             command=f5,
             width=8,
             height=4,
             font=("calibri",10))
f2.grid(row=1, column=3)

f1=tk.Button(root,
             text="Forward\n5",
             command=f5,
             width=8,
             height=4,
             font=("calibri",10))
f1.grid(row=2, column=3)

res_ang=tk.Button(root,
                  text="Reset\nangle",
                  command=resetangle,
                  width=8,
                  height=4,
                  font=("calibri",10))
res_ang.grid(row=6, column=5)

b1=tk.Button(root,
             text="Backward\n5",
             command=b5,
             width=8,
             height=4,
             font=("calibri",10))
b1.grid(row=4, column=3)

b2=tk.Button(root,
             text="Backward\n10",
             command=b10,
             width=8,
             height=4,
             font=("calibri",10))
b2.grid(row=5, column=3)

b3=tk.Button(root,
             text="Backward\n50",
             command=b50,
             width=8,
             height=4,
             font=("calibri",10))
b3.grid(row=6, column=3)

l1=tk.Button(root,
             text="Left\n5",
             command=l5,
             width=8,
             height=4,
             font=("calibri",10))
l1.grid(row=3, column=2)

l2=tk.Button(root,
             text="Left\n10",
             command=l10,
             width=8,
             height=4,
             font=("calibri",10))
l2.grid(row=3, column=1)

l3=tk.Button(root,
             text="Left\n45",
             command=l45,
             width=8,
             height=4,
             font=("calibri",10))
l3.grid(row=3, column=0)

r1=tk.Button(root,
             text="Right\n5",
             command=r5,
             width=8,
             height=4,
             font=("calibri",10))
r1.grid(row=3, column=4)

r2=tk.Button(root,
             text="Right\n10",
             command=r10,
             width=8,
             height=4,
             font=("calibri",10))
r2.grid(row=3, column=5)

r3=tk.Button(root,
             text="Right\n45",
             command=r45,
             width=8,
             height=4,
             font=("calibri",10))
r3.grid(row=3, column=6)

bf=tk.Button(root,
             text="Begin\nfill",
             command=bfill,
             width=8,
             height=4,
             font=("calibri",10))
bf.grid(row=1, column=1)

ef=tk.Button(root,
             text="End\nfill",
             command=efill,
             width=8,
             height=4,
             font=("calibri",10))
ef.grid(row=0, column=1)

clr=tk.Button(root,
             text="Clear\ncanvas",
             command=cls,
             width=8,
             height=4,
             font=("calibri",10),
             bg="red")
clr.grid(row=0, column=6)

ccircle=tk.Button(root,
             text="Create\ncircle",
             command=crc,
             width=8,
             height=4,
             font=("calibri",10))
ccircle.grid(row=3, column=3)

startpen=tk.Button(root,
             text="Pen\ndown",
             command=pd,
             width=8,
             height=4,
             font=("calibri",10))
startpen.grid(row=6, column=1)

stoppen=tk.Button(root,
             text="Pen\nup",
             command=pu,
             width=8,
             height=4,
             font=("calibri",10))
stoppen.grid(row=5, column=1)

posreset=tk.Button(root,
             text="Return to\ncenter",
             command=resetpos,
             width=8,
             height=4,
             font=("calibri",10))
posreset.grid(row=5, column=5)

switchtcolor=tk.Button(root,
             text="Change\nturtle\ncolor",
             command=choosetcolor,
             width=8,
             height=4,
             font=("calibri",10))
switchtcolor.grid(row=2, column=2)

switchbgcolor=tk.Button(root,
             text="Change\nbackground\ncolor",
             command=choosebgcolor,
             width=8,
             height=4,
             font=("calibri",10))
switchbgcolor.grid(row=2, column=4)

reset_tcolour=tk.Button(root,
             text="Default\nturtle\ncolor",
             command=resettcolor,
             width=8,
             height=4,
             font=("calibri",10))
reset_tcolour.grid(row=4, column=2)

reset_bgcolour=tk.Button(root,
             text="Default\nbackground\ncolor",
             command=resetbgcolor,
             width=8,
             height=4,
             font=("calibri",10))
reset_bgcolour.grid(row=4, column=4)

cwidth=tk.Button(root,
             text="Change\npen\nwidth",
             command=changewidth,
             width=8,
             height=4,
             font=("calibri",10))
cwidth.grid(row=0, column=0)

undobutton=tk.Button(root,
             text="Undo",
             command=undo_this,
             width=8,
             height=4,
             font=("calibri",10))
undobutton.grid(row=1, column=5)

speedbutton=tk.Button(root,
             text="Change\nspeed",
             command=speedchange,
             width=8,
             height=4,
             font=("calibri",10))
speedbutton.grid(row=0, column=5)

visibilitybutton=tk.Button(root,
             text="Toggle\nvisibility",
             command=toggle_vis,
             width=8,
             height=4,
             font=("calibri",10))
visibilitybutton.grid(row=6, column=0)

watermark=tk.Button(root,
             text="Hubert G",
             width=8,
             height=4,
             font=("calibri",10))
watermark.grid(row=6, column=6)
root.mainloop()

#toggle pen animation
#

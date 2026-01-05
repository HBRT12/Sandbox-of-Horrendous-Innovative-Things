import turtle
import random

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Turtle Scramble")

# Parameters
NUM_TURTLES = 10
STEPS = 50
COLORS = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "lime", "white"]

# Create turtles
turtles = []
for i in range(NUM_TURTLES):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(random.choice(COLORS))
    t.penup()
    t.goto(random.randint(-200, 200), random.randint(-200, 200))
    t.pendown()
    turtles.append(t)

# Scramble loop
while True:
    for t in turtles:
        angle = random.randint(0, 360)
        distance = random.randint(20, 100)
        t.setheading(angle)
        t.forward(distance)
        t.speed(0)

# Done
turtle.done()

import turtle

# Setup screen and turtle
screen = turtle.Screen()
screen.bgcolor("black")

spiral = turtle.Turtle()
spiral.speed(0)
spiral.pencolor("cyan")

# Parameters
angle = 10
rotations = 10
steps_per_rotation = 360 // angle
step_increment = 0.3
max_cycles = 10  # How many expand/contract loops
offset = 1       # Pixel offset after each loop

# Function to draw one spiral direction
def spiral_pass(forward=True, start_step=1):
    step = start_step
    for _ in range(rotations * steps_per_rotation):
        spiral.forward(step)
        spiral.right(angle)
        if forward:
            step += step_increment
        else:
            step -= step_increment
    return step  # Return final step size for continuity

# Draw cycles
current_step = 1
for _ in range(max_cycles):
    current_step = spiral_pass(forward=True, start_step=current_step)
    current_step = spiral_pass(forward=False, start_step=current_step)
    
    # Offset slightly
    spiral.penup()
    spiral.setheading(0)
    spiral.forward(offset)
    spiral.pendown()

# Exit on click
screen.exitonclick()

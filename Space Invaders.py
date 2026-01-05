import turtle as t
import os
import math

wn=t.Screen()
wn.bgcolor('black')
wn.title('Space Invaders')

border_pen=t.Turtle()
border_pen.speed(0)
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)

for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

border_pen.hideturtle()

#Creating the player turtle

player=t.Turtle()
player.color('blue')
player.shape('triangle')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)
playerspeed=15

#Creating the enemies

enemy=t.Turtle()
enemy.color('#ff0000')
enemy.shape('circle')
enemy.penup()
enemy.speed(0)
enemy.setposition(-200,250)
enemyspeed=2

#Creating bullets

bullet=t.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup()
bullet.speed(9)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()
bulletspeed=20
bulletstate='ready'

def fire_bullet():
    global bulletstate
    print('Bullet fired')
    if bulletstate == 'ready':
        bulletstate = 'fire'
        bullet.showturtle()
        x=player.xcor()
        y=player.ycor()+10
        bullet.setposition(x,y)#

def isCollision(t1,t2):
    distance=math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False

def move_left():
    x=player.xcor()
    x=x-playerspeed
    if x < -280:
        x=-280
    player.setx(x)

def move_right():
    x=player.xcor()
    x=x+playerspeed
    if x > 280:
        x=280
    player.setx(x)

#Creating keybinds

t.listen()
t.onkey(move_left,'Left')
t.onkey(move_right,'Right')
t.onkey(fire_bullet,'space')

while True:
    #Moving the enemy
    x=enemy.xcor()
    x=x+enemyspeed
    enemy.setx(x)

    #Move the enemy left and right
    if enemy.xcor() > 280:
        y=enemy.ycor()
        y=y-40
        enemyspeed = enemyspeed*-1
        enemy.sety(y)
    if enemy.xcor() < -280:
        y=enemy.ycor()
        y=y-40
        enemyspeed=enemyspeed*-1
        enemy.sety(y)

    #move the bullet
    if bulletstate == 'fire':
        y=bullet.ycor()
        y=y+bulletspeed
        bullet.sety(y)

    #Check to see if the bullet is at the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate='ready'

    #Check for collision between bullet and enemy

    if isCollision(bullet,enemy):
        #Reset bullet
        bullet.hideturtle()
        bulletstate = 'ready'
        bullet.setposition(0,-400)

        #Reset the enemy too
        enemy.setposition(-200,250)

    if isCollision(player,enemy):
        player.hideturtle()
        enemy.hideturtle()
        print('Game Over!')
        break

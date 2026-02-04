# Lesson 19: Turtle Animation - Moving Shapes
# Create animated patterns with turtle

import turtle
import time

t = turtle.Turtle()
t.speed(0)
screen = turtle.Screen()
screen.bgcolor("navy")
screen.tracer(0)  # Turn off animation for manual updates

# Animated bouncing ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("yellow")
ball.penup()
ball.goto(-200, 0)

x_speed = 5
y_speed = 3

for _ in range(200):
    # Move ball
    x, y = ball.position()
    x += x_speed
    y += y_speed
    
    # Bounce off walls
    if x > 200 or x < -200:
        x_speed = -x_speed
    if y > 200 or y < -200:
        y_speed = -y_speed
    
    ball.goto(x, y)
    screen.update()
    time.sleep(0.01)

# Rotating star
star = turtle.Turtle()
star.color("white")
star.penup()
star.goto(0, 0)
star.pendown()

for rotation in range(36):
    star.clear()
    star.setheading(rotation * 10)
    for _ in range(5):
        star.forward(100)
        star.right(144)
    screen.update()
    time.sleep(0.1)

# Growing circles
circle_t = turtle.Turtle()
circle_t.color("lime")
circle_t.penup()
circle_t.goto(0, -300)
circle_t.pendown()

for radius in range(10, 100, 5):
    circle_t.circle(radius)
    screen.update()
    time.sleep(0.05)

turtle.done()

# Challenge: Create a pattern where multiple shapes move in different directions

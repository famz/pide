# Lesson 18: Turtle Art - Geometric Patterns
# Create beautiful geometric patterns with turtle

import turtle

t = turtle.Turtle()
t.speed(0)  # Fastest speed
screen = turtle.Screen()
screen.bgcolor("black")
t.color("cyan")

# Pattern 1: Spiral squares
def spiral_squares():
    for i in range(36):
        for _ in range(4):
            t.forward(i * 5)
            t.right(90)
        t.right(10)

# Pattern 2: Colorful circles
def colorful_circles():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    t.penup()
    t.goto(0, -100)
    t.pendown()
    
    for i, color in enumerate(colors):
        t.color(color)
        t.circle(50 + i * 10)
        t.penup()
        t.goto(0, -100 - i * 10)
        t.pendown()

# Pattern 3: Star burst
def star_burst():
    t.penup()
    t.goto(-150, 0)
    t.pendown()
    t.color("yellow")
    
    for i in range(20):
        t.forward(300)
        t.backward(300)
        t.right(360 / 20)

# Run patterns
spiral_squares()
t.penup()
t.goto(200, 0)
t.pendown()
colorful_circles()
t.penup()
t.goto(-150, 0)
t.pendown()
star_burst()

t.hideturtle()
turtle.done()

# Challenge: Create a pattern that draws your initials

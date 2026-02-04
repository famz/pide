# Lesson 20: Turtle Masterpiece - Complex Art
# Create a complex, beautiful drawing combining multiple techniques

import turtle
import random
import math

t = turtle.Turtle()
t.speed(0)
screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)

# Flower function
def draw_flower(x, y, size, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    
    for _ in range(8):
        t.circle(size)
        t.left(45)

# Spiral function
def draw_spiral(x, y, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    
    for i in range(100):
        t.forward(i * 2)
        t.right(91)

# Star field
def draw_stars():
    t.color("white")
    for _ in range(50):
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.dot(3)

# Main composition
colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]

# Draw stars
draw_stars()

# Draw flowers in a circle
for i in range(8):
    angle = i * 45
    x = 150 * math.cos(math.radians(angle))
    y = 150 * math.sin(math.radians(angle))
    draw_flower(x, y, 20, colors[i % len(colors)])

# Draw spirals
for i in range(4):
    angle = i * 90
    x = 100 * math.cos(math.radians(angle))
    y = 100 * math.sin(math.radians(angle))
    draw_spiral(x, y, colors[i * 2])

# Center mandala
t.penup()
t.goto(0, 0)
t.pendown()
t.color("gold")

for i in range(36):
    t.circle(50 + i * 2)
    t.right(10)

screen.update()
t.hideturtle()
turtle.done()

# Challenge: Create your own masterpiece combining different patterns and colors!

# 用 Turtle 画彩虹
import turtle

t = turtle.Turtle()
t.speed(0)
t.width(10)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]

t.penup()
t.goto(-200, -50)
t.pendown()

for i, color in enumerate(colors):
    t.color(color)
    t.circle(150 - i * 15, 180)
    t.penup()
    t.goto(-200, -50 - (i + 1) * 15)
    t.pendown()

t.hideturtle()
turtle.done()

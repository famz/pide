# 用 Turtle 画彩色同心圆
import turtle

t = turtle.Turtle()
t.speed(0)
t.width(3)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]

t.penup()
t.goto(0, -150)
t.pendown()

for i in range(7):
    t.color(colors[i])
    t.circle(30 + i * 20)
    t.penup()
    t.goto(0, -150 - (i + 1) * 20)
    t.pendown()

t.hideturtle()
turtle.done()

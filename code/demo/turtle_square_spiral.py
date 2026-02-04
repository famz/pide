# 用 Turtle 画方形螺旋
import turtle

t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["cyan", "magenta", "yellow", "white"]

for i in range(100):
    t.color(colors[i % 4])
    t.forward(i * 2)
    t.right(91)

t.hideturtle()
turtle.done()

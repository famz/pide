# 用 Turtle 画彩色螺旋
import turtle

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
t = turtle.Turtle()
t.speed(0)

for i in range(180):
    t.pencolor(colors[i % 6])
    t.width(i / 50 + 1)
    t.forward(i)
    t.left(59)

turtle.done()

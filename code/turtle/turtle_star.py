# 用 Turtle 画一颗金色星星
import turtle

t = turtle.Turtle()
t.speed(3)
t.color("gold")
t.width(3)

for i in range(5):
    t.forward(100)
    t.right(144)

t.hideturtle()
turtle.done()

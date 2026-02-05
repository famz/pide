# 用 Turtle 画一朵花
import turtle

t = turtle.Turtle()
t.speed(0)

# 画花瓣
colors = ["red", "orange", "yellow", "pink", "purple", "violet"]
for i in range(6):
    t.color(colors[i])
    t.begin_fill()
    t.circle(50, 60)
    t.left(120)
    t.circle(50, 60)
    t.left(60)
    t.end_fill()

# 画花心
t.penup()
t.goto(0, 0)
t.pendown()
t.color("yellow")
t.dot(30)

t.hideturtle()
turtle.done()

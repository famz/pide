# 用 Turtle 画一棵树（递归）
import turtle

def draw_tree(t, length, depth):
    if depth == 0:
        return

    # 根据深度设置颜色
    if depth <= 2:
        t.color("green")
    else:
        t.color("brown")

    t.width(depth)
    t.forward(length)

    # 画右分支
    t.right(30)
    draw_tree(t, length * 0.7, depth - 1)

    # 画左分支
    t.left(60)
    draw_tree(t, length * 0.7, depth - 1)

    # 返回
    t.right(30)
    t.backward(length)

t = turtle.Turtle()
t.speed(0)
t.left(90)
t.penup()
t.goto(0, -150)
t.pendown()

draw_tree(t, 80, 7)

t.hideturtle()
turtle.done()

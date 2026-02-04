# 猜数字游戏
import random

secret = random.randint(1, 100)
print("我想了一个 1-100 之间的数字，你来猜！")

while True:
    guess = int(input("请输入你的猜测: "))
    if guess < secret:
        print("太小了，再试试！")
    elif guess > secret:
        print("太大了，再试试！")
    else:
        print("恭喜你，猜对了！")
        break

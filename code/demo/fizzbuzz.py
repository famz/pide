# FizzBuzz - 经典编程练习
# 规则: 3的倍数打印Fizz, 5的倍数打印Buzz, 都是则打印FizzBuzz

for i in range(1, 31):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

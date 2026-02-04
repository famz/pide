# 简单计算器
print("简单计算器")
print("支持: +, -, *, /")

while True:
    expr = input("请输入算式 (如 3+5)，或输入 q 退出: ")
    if expr.lower() == 'q':
        print("再见！")
        break
    try:
        # 注意：eval 在真实项目中要小心使用
        result = eval(expr)
        print(f"结果: {result}")
    except:
        print("算式有误，请重试")

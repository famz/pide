# Lesson 15: Calculator Functions
# Build a calculator with reusable functions

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b

def power(a, b):
    return a ** b

def calculator():
    print("=" * 40)
    print("CALCULATOR")
    print("=" * 40)
    print("Operations: +, -, *, /, ^")
    
    num1 = float(input("Enter first number: "))
    operation = input("Enter operation (+, -, *, /, ^): ")
    num2 = float(input("Enter second number: "))
    
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
        "^": power
    }
    
    if operation in operations:
        result = operations[operation](num1, num2)
        print(f"\n{num1} {operation} {num2} = {result}")
    else:
        print("Invalid operation!")

calculator()

# Challenge: Add more operations like square root, percentage, etc.

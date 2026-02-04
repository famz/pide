# Lesson 4: Math Magic Tricks
# Perform some fun math tricks and calculations

# Trick 1: Multiply any number by 9 using finger trick
number = 7
result = number * 9
print(f"Trick: {number} × 9 = {result}")
print(f"Check: {number} × 9 = {number * 9}")

# Trick 2: Check if a number is divisible by 3
# (Sum of digits divisible by 3 means the number is divisible by 3)
test_number = 123
digit_sum = sum(int(d) for d in str(test_number))
is_divisible = digit_sum % 3 == 0
print(f"\nIs {test_number} divisible by 3?")
print(f"Sum of digits: {digit_sum}")
print(f"Answer: {is_divisible}")

# Trick 3: Calculate the area of a circle
radius = 5
pi = 3.14159
area = pi * radius ** 2
print(f"\nCircle with radius {radius}:")
print(f"Area = π × r² = {pi} × {radius}² = {area:.2f}")

# Trick 4: Find the factorial of a number
n = 5
factorial = 1
for i in range(1, n + 1):
    factorial *= i
print(f"\n{n}! (factorial) = {factorial}")

# Challenge: Calculate the volume of a sphere (V = 4/3 × π × r³)
# Use radius = 3

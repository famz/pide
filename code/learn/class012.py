# Lesson 12: Pattern Art Generator
# Create beautiful patterns using loops

# Pattern 1: Number triangle
print("Pattern 1: Number Triangle")
for i in range(1, 6):
    print(str(i) * i)

# Pattern 2: Star pyramid
print("\nPattern 2: Star Pyramid")
for i in range(1, 6):
    spaces = " " * (5 - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)

# Pattern 3: Diamond pattern
print("\nPattern 3: Diamond")
size = 5
for i in range(size):
    spaces = " " * (size - i - 1)
    stars = "*" * (2 * i + 1)
    print(spaces + stars)
for i in range(size - 2, -1, -1):
    spaces = " " * (size - i - 1)
    stars = "*" * (2 * i + 1)
    print(spaces + stars)

# Pattern 4: Multiplication table
print("\nPattern 4: Multiplication Table (5x5)")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:3}", end=" ")
    print()

# Pattern 5: Checkerboard
print("\nPattern 5: Checkerboard")
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            print("█", end="")
        else:
            print(" ", end="")
    print()

# Challenge: Create a pattern that spells your name vertically

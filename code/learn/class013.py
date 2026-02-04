# Lesson 13: Number Sequence Generator
# Generate interesting number sequences

# Fibonacci sequence
print("Fibonacci Sequence (first 10 numbers):")
a, b = 0, 1
count = 0
while count < 10:
    print(a, end=" ")
    a, b = b, a + b
    count += 1

# Prime numbers
print("\n\nPrime Numbers (first 10):")
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

count = 0
num = 2
while count < 10:
    if is_prime(num):
        print(num, end=" ")
        count += 1
    num += 1

# Perfect squares
print("\n\nPerfect Squares (1-10):")
for i in range(1, 11):
    print(f"{i}² = {i*i}", end="  ")

# Triangular numbers
print("\n\nTriangular Numbers (first 10):")
total = 0
for i in range(1, 11):
    total += i
    print(total, end=" ")

# Challenge: Generate the sequence: 1, 4, 9, 16, 25... (what is this sequence?)

# Lesson 6: Password Generator
# Generate random passwords with different complexity levels

import random
import string

# Simple password: random letters
def generate_simple_password(length=8):
    password = ""
    for _ in range(length):
        password += random.choice(string.ascii_letters)
    return password

# Medium password: letters and numbers
def generate_medium_password(length=10):
    password = ""
    chars = string.ascii_letters + string.digits
    for _ in range(length):
        password += random.choice(chars)
    return password

# Strong password: letters, numbers, and special characters
def generate_strong_password(length=12):
    password = ""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    for _ in range(length):
        password += random.choice(chars)
    return password

# Generate passwords
print("Simple Password (8 chars):", generate_simple_password())
print("Medium Password (10 chars):", generate_medium_password())
print("Strong Password (12 chars):", generate_strong_password())

# Create a memorable password from words
words = ["sun", "moon", "star", "sky", "cloud"]
memorable = random.choice(words) + str(random.randint(10, 99)) + random.choice(words)
print(f"\nMemorable Password: {memorable}")

# Challenge: Create a function that checks password strength
# Return "weak", "medium", or "strong" based on length and character types

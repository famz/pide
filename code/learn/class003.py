# Lesson 3: Number Guessing Game
# A simple number guessing game with hints

import random

secret_number = random.randint(1, 100)
attempts = 0
max_attempts = 7

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print(f"You have {max_attempts} attempts to guess it!")

while attempts < max_attempts:
    guess = int(input(f"\nAttempt {attempts + 1}: Enter your guess: "))
    attempts += 1
    
    if guess == secret_number:
        print(f"🎉 Congratulations! You guessed it in {attempts} attempts!")
        break
    elif guess < secret_number:
        difference = secret_number - guess
        if difference > 20:
            print("Too low! Try much higher.")
        else:
            print("Too low! You're getting close.")
    else:
        difference = guess - secret_number
        if difference > 20:
            print("Too high! Try much lower.")
        else:
            print("Too high! You're getting close.")
    
    if attempts < max_attempts:
        print(f"You have {max_attempts - attempts} attempts left.")

if attempts >= max_attempts and guess != secret_number:
    print(f"\nGame Over! The number was {secret_number}")

# Challenge: Add a difficulty level (easy: 1-50, hard: 1-200)
# Let the player choose before starting

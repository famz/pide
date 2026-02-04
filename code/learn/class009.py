# Lesson 9: Rock Paper Scissors Game
# Build a classic game with computer opponent

import random

choices = ["rock", "paper", "scissors"]
computer_choice = random.choice(choices)

print("Rock Paper Scissors Game!")
print("Choose: rock, paper, or scissors")
player_choice = input("Your choice: ").lower()

if player_choice not in choices:
    print("Invalid choice! Please choose rock, paper, or scissors.")
else:
    print(f"\nYou chose: {player_choice}")
    print(f"Computer chose: {computer_choice}\n")
    
    if player_choice == computer_choice:
        print("It's a tie! 🤝")
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        print("You win! 🎉")
    else:
        print("Computer wins! 💻")

# Challenge: Add a best-of-3 mode where you play until someone wins 2 rounds

# Lesson 1: Personal Info Card Generator
# Create a program that generates a personalized info card

name = "Alice"
age = 12
favorite_color = "blue"
favorite_food = "pizza"
hobby = "coding"

# Create a decorative info card
print("=" * 40)
print(" " * 10 + "MY INFO CARD")
print("=" * 40)
print(f"Name: {name}")
print(f"Age: {age} years old")
print(f"Favorite Color: {favorite_color}")
print(f"Favorite Food: {favorite_food}")
print(f"Hobby: {hobby}")
print("=" * 40)

# Calculate and display some fun facts
days_old = age * 365
print(f"\nFun Fact: You are approximately {days_old} days old!")
print(f"Your name has {len(name)} letters!")

# Challenge: Modify the variables above to create your own info card
# Then add two more variables (like favorite_game or dream_job) and display them

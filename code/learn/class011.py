# Lesson 11: Adventure Decision Tree
# Create a text-based adventure with multiple paths

print("=" * 50)
print("MYSTERY ISLAND ADVENTURE")
print("=" * 50)
print("\nYou wake up on a mysterious island...")

# First decision
print("\nYou see two paths ahead:")
print("1. Go into the dark forest")
print("2. Walk along the beach")
choice1 = input("Choose (1 or 2): ")

if choice1 == "1":
    print("\nYou enter the forest and find an old map!")
    print("The map shows a treasure location.")
    print("\nWhat do you do?")
    print("1. Follow the map")
    print("2. Ignore it and keep walking")
    choice2 = input("Choose (1 or 2): ")
    
    if choice2 == "1":
        print("\n🎉 You find a treasure chest full of gold coins!")
        print("You win!")
    else:
        print("\nYou get lost in the forest...")
        print("Game Over!")
        
elif choice1 == "2":
    print("\nYou walk along the beach and find a boat!")
    print("The boat looks seaworthy.")
    print("\nWhat do you do?")
    print("1. Get in the boat and sail away")
    print("2. Search the beach for supplies first")
    choice2 = input("Choose (1 or 2): ")
    
    if choice2 == "1":
        print("\nYou sail away and reach civilization!")
        print("You are rescued! 🚢")
    else:
        print("\nYou find a message in a bottle with coordinates!")
        print("You follow them and find help!")
        print("You are saved! 🏝️")
else:
    print("\nInvalid choice! You stand still and nothing happens...")

# Challenge: Expand the adventure with more branches and choices

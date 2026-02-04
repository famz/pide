# Lesson 7: Interactive Story Generator
# Create an interactive story where user choices affect the outcome

print("=" * 50)
print("ADVENTURE STORY GENERATOR")
print("=" * 50)

name = input("Enter your character's name: ")
place = input("Enter a place (forest/castle/beach): ")
item = input("Enter a magical item: ")

print("\n" + "=" * 50)
print("YOUR STORY:")
print("=" * 50)

story = f"""
Once upon a time, {name} was walking through a {place}.
Suddenly, they found a glowing {item}!

{name} picked up the {item} and felt a strange power.
The {item} began to glow brighter and brighter...

What happens next?
1. The {item} opens a portal to another world
2. {name} gains magical powers
3. The {item} disappears and leaves a map

Choose your ending (1, 2, or 3): """
choice = input(story)

endings = {
    "1": f"{name} steps through the portal and discovers a magical kingdom!",
    "2": f"{name} can now cast spells and becomes a powerful wizard!",
    "3": f"{name} follows the map and finds a hidden treasure!"
}

print("\n" + endings.get(choice, "The story continues..."))

# Challenge: Add more choices and create a branching story with multiple paths

# Lesson 5: Text Art Generator
# Create ASCII art and text patterns

# Create a name banner
name = "PYTHON"
banner = "*" * (len(name) + 4)
print(banner)
print(f"* {name} *")
print(banner)

# Create a word pyramid
word = "CODE"
for i in range(len(word)):
    print(word[:i+1])

# Create a reverse word
original = "HELLO"
reversed_word = original[::-1]
print(f"\n{original} backwards is {reversed_word}")

# Create a word with alternating case
text = "programming"
alternating = ""
for i, char in enumerate(text):
    if i % 2 == 0:
        alternating += char.upper()
    else:
        alternating += char.lower()
print(f"\n{alternating}")

# Count vowels in a word
word = "education"
vowels = "aeiouAEIOU"
vowel_count = sum(1 for char in word if char in vowels)
print(f"\n'{word}' has {vowel_count} vowels")

# Challenge: Create a function that takes a word and creates a box around it
# Example: "HI" becomes:
# ****
# *HI*
# ****

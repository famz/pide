# Lesson 14: Password Cracker Simulation
# Simulate trying different passwords until finding the right one

import random
import string

# Generate a random password
target_password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
print(f"Target password: {target_password} (hidden in real scenario)")
print("Simulating password cracker...\n")

attempts = 0
max_attempts = 10000
found = False

# Try random combinations
while attempts < max_attempts and not found:
    guess = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    attempts += 1
    
    if guess == target_password:
        found = True
        print(f"✓ Password found: {guess}")
        print(f"Attempts needed: {attempts}")
        break
    
    # Show progress every 1000 attempts
    if attempts % 1000 == 0:
        print(f"Tried {attempts} combinations... still searching")

if not found:
    print(f"Could not find password in {max_attempts} attempts")

# Brute force approach (systematic)
print("\n" + "=" * 50)
print("Systematic Brute Force Approach:")
print("=" * 50)

target = "abc"
chars = string.ascii_lowercase
attempts = 0
found = False

for c1 in chars:
    for c2 in chars:
        for c3 in chars:
            guess = c1 + c2 + c3
            attempts += 1
            if guess == target:
                print(f"✓ Found '{target}' in {attempts} attempts")
                found = True
                break
        if found:
            break
    if found:
        break

# Challenge: Add a timer to see how long each method takes

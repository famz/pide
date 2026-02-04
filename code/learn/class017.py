# Lesson 17: Game Helper Functions
# Create reusable functions for game mechanics

import random

def roll_dice(sides=6):
    """Roll a dice with specified number of sides"""
    return random.randint(1, sides)

def flip_coin():
    """Flip a coin"""
    return random.choice(["Heads", "Tails"])

def generate_loot():
    """Generate random loot"""
    items = ["sword", "shield", "potion", "gold coin", "gem", "scroll"]
    return random.choice(items)

def calculate_damage(base_damage, crit_chance=0.1):
    """Calculate damage with critical hit chance"""
    is_crit = random.random() < crit_chance
    if is_crit:
        return base_damage * 2, True
    return base_damage, False

def battle_simulation(player_health=100, enemy_health=80):
    """Simulate a simple battle"""
    print("=" * 40)
    print("BATTLE SIMULATION")
    print("=" * 40)
    
    turn = 1
    while player_health > 0 and enemy_health > 0:
        print(f"\nTurn {turn}")
        print(f"Player HP: {player_health} | Enemy HP: {enemy_health}")
        
        # Player attack
        damage, crit = calculate_damage(20, 0.2)
        if crit:
            print(f"💥 CRITICAL HIT! Player deals {damage} damage!")
        else:
            print(f"⚔️ Player deals {damage} damage")
        enemy_health -= damage
        
        if enemy_health <= 0:
            print("\n🎉 Player wins!")
            break
        
        # Enemy attack
        enemy_damage = random.randint(10, 25)
        print(f"👹 Enemy deals {enemy_damage} damage")
        player_health -= enemy_damage
        
        if player_health <= 0:
            print("\n💀 Enemy wins!")
            break
        
        turn += 1

# Test the functions
print("Dice roll (6-sided):", roll_dice())
print("Coin flip:", flip_coin())
print("Loot found:", generate_loot())

damage, crit = calculate_damage(15)
print(f"Damage: {damage}, Critical: {crit}")

battle_simulation()

# Challenge: Add a function to level up characters with stat increases

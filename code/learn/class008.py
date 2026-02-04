# Lesson 8: Quiz Game
# Build an interactive quiz with scoring

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
        "correct": "B"
    },
    {
        "question": "What is 15 × 3?",
        "options": ["A) 35", "B) 40", "C) 45", "D) 50"],
        "correct": "C"
    },
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["A) Venus", "B) Earth", "C) Mercury", "D) Mars"],
        "correct": "C"
    },
    {
        "question": "What is the largest ocean?",
        "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
        "correct": "D"
    }
]

score = 0
total = len(questions)

print("=" * 50)
print("QUIZ GAME")
print("=" * 50)
print(f"Answer {total} questions. Good luck!\n")

for i, q in enumerate(questions, 1):
    print(f"Question {i}: {q['question']}")
    for option in q['options']:
        print(f"  {option}")
    
    answer = input("Your answer (A/B/C/D): ").upper()
    
    if answer == q['correct']:
        print("✓ Correct!\n")
        score += 1
    else:
        print(f"✗ Wrong! The correct answer is {q['correct']}\n")

print("=" * 50)
print(f"QUIZ COMPLETE!")
print(f"Your score: {score}/{total} ({score*100//total}%)")
print("=" * 50)

# Challenge: Add more questions and create different difficulty levels

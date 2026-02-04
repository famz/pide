# Lesson 10: Grade Calculator
# Calculate grades and provide feedback based on scores

def calculate_grade(score):
    """Calculate letter grade and feedback"""
    if score >= 90:
        return "A", "Excellent work! 🌟"
    elif score >= 80:
        return "B", "Good job! 👍"
    elif score >= 70:
        return "C", "Not bad, keep improving! 📚"
    elif score >= 60:
        return "D", "You passed, but need more practice. 💪"
    else:
        return "F", "Don't give up! Study harder next time. 📖"

# Get scores for different subjects
subjects = ["Math", "Science", "English", "History"]
scores = {}

print("Grade Calculator")
print("=" * 40)

for subject in subjects:
    score = int(input(f"Enter {subject} score (0-100): "))
    scores[subject] = score

# Calculate average
total = sum(scores.values())
average = total / len(scores)
grade, feedback = calculate_grade(average)

# Display results
print("\n" + "=" * 40)
print("REPORT CARD")
print("=" * 40)
for subject, score in scores.items():
    letter, _ = calculate_grade(score)
    print(f"{subject}: {score} ({letter})")

print(f"\nAverage: {average:.1f}")
print(f"Overall Grade: {grade}")
print(feedback)
print("=" * 40)

# Challenge: Add weighted grades (some subjects count more than others)

Simple AI Grading Assistant

# Function to find grade from marks
def get_grade(marks):
    if marks >= 90:
        return "A+", 10
    elif marks >= 80:
        return "A", 9
    elif marks >= 70:
        return "B+", 8
    elif marks >= 60:
        return "B", 7
    elif marks >= 50:
        return "C", 6
    elif marks >= 40:
        return "D", 5
    else:
        return "F", 0

# Input from user
n = int(input("Enter number of subjects: "))
subjects = []
total_marks = 0
total_points = 0

for i in range(n):
    name = input(f"Enter subject {i+1} name: ")
    marks = int(input(f"Enter marks in {name}: "))
    grade, point = get_grade(marks)
    subjects.append((name, marks, grade))
    total_marks += marks
    total_points += point

# Calculate results
percentage = total_marks / n
gpa = total_points / n

# Show report
print("\n--- Report Card ---")
for s in subjects:
    print(f"{s[0]}: {s[1]} marks → Grade {s[2]}")
print(f"\nAverage %: {percentage:.2f}")
print(f"GPA (10-point): {gpa:.2f}")

# Insights
print(" AI Assistant Insights")
if percentage >= 85:
    print("Excellent keep it up")
elif percentage >= 70:
    print("Try to practice more ")
else:
    print("Needs improvement")

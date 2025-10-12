study_hours = [2, 4, 6, 8, 10]
pass_fail = [0, 0, 1, 1, 1]

print("Dataset:")
for i in range(len(study_hours)):
    print(f"Student {i+1}: {study_hours[i]} hours → {'Pass' if pass_fail[i] else 'Fail'}")

print("\nStep 1: Find possible split points")
splits = [3, 5, 7, 9]   
print("Possible splits:", splits)

print("\nStep 2: Calculate Gini impurity for each split")

best_split = None
lowest_gini = 1.0

for s in splits:
    left = [pass_fail[i] for i in range(len(study_hours)) if study_hours[i] <= s]
    right = [pass_fail[i] for i in range(len(study_hours)) if study_hours[i] > s]
    
    def gini(group):
        if len(group) == 0:
            return 0
        p = sum(group)/len(group)
        q = 1 - p
        return 1 - (p**2 + q**2)

    gini_left = gini(left)
    gini_right = gini(right)
    weighted_gini = (len(left)*gini_left + len(right)*gini_right) / len(study_hours)

    print(f"Split at {s}: Left={left}, Right={right}, Weighted Gini={weighted_gini:.3f}")

    if weighted_gini < lowest_gini:
        lowest_gini = weighted_gini
        best_split = s

print("\nBest Split is at:", best_split, "with Gini:", round(lowest_gini, 3))

print("\nDecision Tree:")
print(f"If Study Hours ≤ {best_split} → Predict: Fail")
print(f"If Study Hours > {best_split} → Predict: Pass")

print("\nPredictions:")
for h in [1, 3, 5, 7, 9, 11]:
    if h <= best_split:
        print(f"Study {h} hours → Fail")
    else:
        print(f"Study {h} hours → Pass")

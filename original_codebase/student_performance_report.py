import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix
)

folder = Path(__file__).resolve().parent.parent / "results"
input_file = folder / "student_fair_predictions.csv"

# Select k=5, the highest observed accuracy in our fair evaluation
selected_k = 5

with open(input_file, encoding="utf-8", newline="") as file:
    rows = [
        row for row in csv.DictReader(file)
        if int(row["k"]) == selected_k
    ]

assert len(rows) == 50, "Expected 50 test predictions"

actual = [row["true_label"] for row in rows]
predicted = [row["predicted_label"] for row in rows]

labels = [
    "enrolment",
    "fees",
    "assessment",
    "campus_services",
    "it_support"
]

print(f"=== STUDENT ENQUIRY EVALUATION (k={selected_k}) ===")
print(f"Test examples: {len(rows)}")
print(f"Accuracy: {accuracy_score(actual, predicted):.2%}")

print("\nClassification report:")
print(
    classification_report(
        actual,
        predicted,
        labels=labels,
        zero_division=0,
        digits=3
    )
)

# Generate confusion matrix
matrix = confusion_matrix(actual, predicted, labels=labels)

display_labels = [
    "Enrolment",
    "Fees",
    "Assessment",
    "Campus",
    "IT Support"
]

fig, ax = plt.subplots(figsize=(8, 6))

disp = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=display_labels
)

disp.plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)

plt.title(f"Student Enquiry Classification — k={selected_k}")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

figure_file = folder / "student_confusion_matrix.png"
plt.savefig(figure_file, dpi=200)
plt.close()

print("\nConfusion matrix saved to:", figure_file)

# Save misclassified examples
error_file = folder / "student_errors_k5.csv"

with open(error_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["text", "true_label", "predicted_label"]
    )
    writer.writeheader()

    for row in rows:
        if row["true_label"] != row["predicted_label"]:
            writer.writerow({
                "text": row["text"],
                "true_label": row["true_label"],
                "predicted_label": row["predicted_label"]
            })

errors = sum(a != p for a, p in zip(actual, predicted))

print("Incorrect predictions:", errors)
print("Error examples saved to:", error_file)
import csv
from collections import Counter
from pathlib import Path

from compressors import DefaultCompressor
from experiments import KnnExpText
from utils import NCD, agg_by_concat_space

# Locate the prepared student dataset
data_folder = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "student_enquiries"
    / "classifier_dataset"
)

def load_data(filename):
    pairs = []

    with open(filename, encoding="utf-8") as file:
        for line in file:
            label, text = line.rstrip("\n").split("\t", 1)
            pairs.append((label, text))

    return pairs


train_pairs = load_data(data_folder / "train.txt")
test_pairs = load_data(data_folder / "test.txt")

train_labels = [label for label, text in train_pairs]
train_texts = [text for label, text in train_pairs]

test_labels = [label for label, text in test_pairs]
test_texts = [text for label, text in test_pairs]

# Use the original implementation
compressor = DefaultCompressor("gzip")

classifier = KnnExpText(
    agg_by_concat_space,
    compressor,
    NCD
)

classifier.calc_dis(test_texts, train_data=train_texts)

# Replicate the original evaluation, including its tie handling
predictions, correct_flags = classifier.calc_acc(
    k=2,
    label=test_labels,
    train_label=train_labels
)

results = []

for text, actual, predicted, correct in zip(
    test_texts, test_labels, predictions, correct_flags
):
    results.append({
        "text": text,
        "true_label": actual,
        "predicted_label": predicted,
        "correct": bool(correct)
    })

output_file = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "student_predictions_original.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["text", "true_label", "predicted_label", "correct"]
    )
    writer.writeheader()
    writer.writerows(results)

correct_count = sum(correct_flags)

print("\n=== ORIGINAL CLASSIFIER ERROR ANALYSIS ===")
print("Total test enquiries:", len(results))
print("Correct predictions:", correct_count)
print("Incorrect predictions:", len(results) - correct_count)
print(f"Accuracy: {correct_count / len(results):.2%}")

print("\nErrors by category:")

for label in sorted(set(test_labels)):
    errors = sum(
        row["true_label"] == label and not row["correct"]
        for row in results
    )
    print(f"{label}: {errors}")

print("\nMisclassified enquiries:")

for row in results:
    if not row["correct"]:
        print(f"\nText: {row['text']}")
        print(f"Actual: {row['true_label']}")
        print(f"Predicted: {row['predicted_label']}")

print("\nResults saved to:", output_file)
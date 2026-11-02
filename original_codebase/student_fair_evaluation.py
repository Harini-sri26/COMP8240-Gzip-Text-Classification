import csv
from collections import Counter
from pathlib import Path

import numpy as np

from compressors import DefaultCompressor
from experiments import KnnExpText
from utils import NCD, agg_by_concat_space

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

assert len(train_pairs) == 200
assert len(test_pairs) == 50

classifier = KnnExpText(
    agg_by_concat_space,
    DefaultCompressor("gzip"),
    NCD
)

classifier.calc_dis(test_texts, train_data=train_texts)

results = []

for k in [1, 2, 3, 5]:
    correct = 0

    for i, distances in enumerate(classifier.distance_matrix):
        nearest_indices = np.argsort(distances, kind="stable")[:k]
        nearest_labels = [train_labels[j] for j in nearest_indices]

        counts = Counter(nearest_labels)
        highest_vote = max(counts.values())

        # Resolve voting ties using the closest neighbour among tied classes.
        # The true test label is never used to choose a prediction.
        tied_labels = {
            label for label, count in counts.items()
            if count == highest_vote
        }

        predicted = next(
            label for label in nearest_labels
            if label in tied_labels
        )

        actual = test_labels[i]
        is_correct = predicted == actual
        correct += is_correct

        results.append({
            "k": k,
            "text": test_texts[i],
            "true_label": actual,
            "predicted_label": predicted,
            "correct": is_correct
        })

    print(f"k={k}: {correct}/50 correct, accuracy={correct / 50:.2%}")

output_file = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "student_fair_predictions.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["k", "text", "true_label", "predicted_label", "correct"]
    )
    writer.writeheader()
    writer.writerows(results)

print("\nSaved predictions to:", output_file)
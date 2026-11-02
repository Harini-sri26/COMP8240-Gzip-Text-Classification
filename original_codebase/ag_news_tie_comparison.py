import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from torchtext.datasets import AG_NEWS

from compressors import DefaultCompressor
from experiments import KnnExpText
from utils import NCD, agg_by_concat_space


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "ag_news_replication"
DATA_DIR = PROJECT_ROOT / "data"

K = 2


def load_saved_sample(split, per_class):
    """Reconstruct selected examples in their original saved order."""

    filename = RESULTS_DIR / (
        f"AG_NEWS_{split}_indicies_{per_class}per_class.npy"
    )
    indices = np.load(filename)

    positions = {
        int(index): position
        for position, index in enumerate(indices)
    }

    selected = [None] * len(indices)

    for index, example in enumerate(
        AG_NEWS(root=str(DATA_DIR), split=split)
    ):
        if index in positions:
            selected[positions[index]] = example

    if any(example is None for example in selected):
        raise ValueError(f"Could not reconstruct {split} examples")

    labels = [label for label, text in selected]
    texts = [text for label, text in selected]

    return texts, labels


print("=== LOADING SAVED AG NEWS SAMPLES ===")

train_texts, train_labels = load_saved_sample("train", 50)
test_texts, test_labels = load_saved_sample("test", 20)

print("Training examples:", len(train_texts))
print("Testing examples:", len(test_texts))

print("\n=== CALCULATING ORIGINAL GZIP/NCD DISTANCES ===")

classifier = KnnExpText(
    agg_by_concat_space,
    DefaultCompressor("gzip"),
    NCD
)

classifier.calc_dis(test_texts, train_data=train_texts)

distances = np.asarray(classifier.distance_matrix)

assert distances.shape == (80, 200), (
    f"Unexpected distance matrix shape: {distances.shape}"
)

np.save(RESULTS_DIR / "ag_news_distances.npy", distances)

print("Distance matrix shape:", distances.shape)

print("\n=== ORIGINAL EVALUATION ===")

original_predictions, original_correct = classifier.calc_acc(
    k=K,
    label=test_labels,
    train_label=train_labels
)

print("\n=== LABEL-INDEPENDENT EVALUATION ===")

fair_predictions = []
tie_count = 0

for row in distances:
    # Stable ordering gives deterministic neighbour selection.
    neighbour_indices = np.argsort(row, kind="stable")[:K]
    neighbour_labels = [
        train_labels[index]
        for index in neighbour_indices
    ]

    votes = Counter(neighbour_labels)
    highest_vote = max(votes.values())

    tied_labels = {
        label
        for label, count in votes.items()
        if count == highest_vote
    }

    if len(tied_labels) > 1:
        tie_count += 1

    # Resolve tied votes using the closest neighbour.
    prediction = next(
        label
        for label in neighbour_labels
        if label in tied_labels
    )

    fair_predictions.append(prediction)

original_accuracy = np.mean(original_correct)
fair_accuracy = np.mean(
    np.asarray(fair_predictions) == np.asarray(test_labels)
)

changed_predictions = sum(
    original != fair
    for original, fair in zip(
        original_predictions, fair_predictions
    )
)

print(f"Original accuracy: {original_accuracy:.2%}")
print(f"Fair accuracy: {fair_accuracy:.2%}")
print("Tied-vote cases:", tie_count)
print("Changed predictions:", changed_predictions)

output_file = RESULTS_DIR / "ag_news_tie_comparison.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "true_label",
        "original_prediction",
        "fair_prediction",
        "original_correct",
        "fair_correct"
    ])

    for actual, original, fair in zip(
        test_labels,
        original_predictions,
        fair_predictions
    ):
        writer.writerow([
            actual,
            original,
            fair,
            original == actual,
            fair == actual
        ])

print("\nResults saved to:", output_file)
print("Distance matrix saved to:",
      RESULTS_DIR / "ag_news_distances.npy")
import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from compressors import DefaultCompressor
from experiments import KnnExpText
from utils import NCD, agg_by_concat_space


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "student_enquiries"
SPLIT_DIR = DATA_DIR / "classifier_dataset"
RESULTS_DIR = ROOT / "results"

K_VALUES = [1, 2, 3, 5]
SEED = 42


def load_pairs(path):
    pairs = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            label, text = line.rstrip("\n").split("\t", 1)
            pairs.append((label, text))

    return pairs


def predict_from_distances(distances, reference_labels, k):
    predictions = []

    for row in distances:
        nearest_indices = np.argsort(row, kind="stable")[:k]
        nearest_labels = [reference_labels[i] for i in nearest_indices]

        counts = Counter(nearest_labels)
        max_votes = max(counts.values())

        tied_labels = {
            label
            for label, count in counts.items()
            if count == max_votes
        }

        # Use the closest neighbour among tied classes.
        prediction = next(
            label for label in nearest_labels
            if label in tied_labels
        )

        predictions.append(prediction)

    return predictions


def calculate_distances(query_texts, reference_texts):
    classifier = KnnExpText(
        agg_by_concat_space,
        DefaultCompressor("gzip"),
        NCD
    )

    classifier.calc_dis(
        query_texts,
        train_data=reference_texts
    )

    return np.asarray(classifier.distance_matrix)


# --------------------------------------------------
# 1. Load original dataset and existing split
# --------------------------------------------------

with (DATA_DIR / "student_enquiries.csv").open(
    newline="", encoding="utf-8-sig"
) as file:
    all_rows = list(csv.DictReader(file))

train_pairs = load_pairs(SPLIT_DIR / "train.txt")
test_pairs = load_pairs(SPLIT_DIR / "test.txt")

assert len(train_pairs) == 200
assert len(test_pairs) == 50

# Match each training example back to its topic.
# Each enquiry text is unique in the dataset.
row_lookup = {
    (row["label"], row["text"]): row
    for row in all_rows
}

train_rows = []

for label, text in train_pairs:
    key = (label, text)

    if key not in row_lookup:
        raise ValueError(f"Training example not found: {key}")

    train_rows.append(row_lookup[key])

assert len(train_rows) == 200


# --------------------------------------------------
# 2. Create a topic-disjoint internal validation split
# --------------------------------------------------

groups = defaultdict(list)

for row in train_rows:
    groups[(row["label"], row["source_topic"])].append(row)

rng = random.Random(SEED)

internal_train = []
validation = []

for label in sorted({row["label"] for row in train_rows}):
    topics = sorted(
        topic
        for class_name, topic in groups
        if class_name == label
    )

    assert len(topics) == 8

    rng.shuffle(topics)

    for topic in topics[:6]:
        internal_train.extend(groups[(label, topic)])

    for topic in topics[6:]:
        validation.extend(groups[(label, topic)])

rng.shuffle(internal_train)
rng.shuffle(validation)

train_topics = {
    (row["label"], row["source_topic"])
    for row in internal_train
}

validation_topics = {
    (row["label"], row["source_topic"])
    for row in validation
}

assert train_topics.isdisjoint(validation_topics)
assert len(internal_train) == 150
assert len(validation) == 50

print("=== INTERNAL VALIDATION SPLIT ===")
print("Internal training examples:", len(internal_train))
print("Validation examples:", len(validation))
print("Topic leakage check: PASSED")


# --------------------------------------------------
# 3. Evaluate k values using validation data only
# --------------------------------------------------

internal_train_texts = [row["text"] for row in internal_train]
internal_train_labels = [row["label"] for row in internal_train]

validation_texts = [row["text"] for row in validation]
validation_labels = [row["label"] for row in validation]

print("\n=== CALCULATING VALIDATION DISTANCES ===")

validation_distances = calculate_distances(
    validation_texts,
    internal_train_texts
)

validation_results = {}

for k in K_VALUES:
    predictions = predict_from_distances(
        validation_distances,
        internal_train_labels,
        k
    )

    accuracy = np.mean(
        np.asarray(predictions) == np.asarray(validation_labels)
    )

    validation_results[k] = float(accuracy)

    print(f"k={k}: validation accuracy={accuracy:.2%}")

# Highest validation accuracy wins.
# If tied, choose the smallest k.
selected_k = min(
    K_VALUES,
    key=lambda k: (-validation_results[k], k)
)

print("\nSelected k:", selected_k)


# --------------------------------------------------
# 4. Final evaluation using the existing test set
# --------------------------------------------------

train_texts = [text for label, text in train_pairs]
train_labels = [label for label, text in train_pairs]

test_texts = [text for label, text in test_pairs]
test_labels = [label for label, text in test_pairs]

print("\n=== FINAL TEST EVALUATION ===")

test_distances = calculate_distances(
    test_texts,
    train_texts
)

test_predictions = predict_from_distances(
    test_distances,
    train_labels,
    selected_k
)

test_accuracy = float(np.mean(
    np.asarray(test_predictions) == np.asarray(test_labels)
))

print(f"Validation-selected k: {selected_k}")
print(f"Final test accuracy: {test_accuracy:.2%}")


# --------------------------------------------------
# 5. Save results separately
# --------------------------------------------------

RESULTS_DIR.mkdir(exist_ok=True)

output_path = RESULTS_DIR / "student_validation_selection.csv"

with output_path.open(
    "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "selected_k",
        "validation_k",
        "validation_accuracy",
        "final_test_accuracy"
    ])

    for k in K_VALUES:
        writer.writerow([
            selected_k,
            k,
            validation_results[k],
            test_accuracy
        ])

print("\nResults saved to:", output_path)
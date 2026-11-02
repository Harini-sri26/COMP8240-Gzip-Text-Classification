import csv
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from compressors import DefaultCompressor
from experiments import KnnExpText
from utils import NCD, agg_by_concat_space

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

SEEDS = [42, 123, 2026, 7, 99]
K = 5

# Locate the GitHub repository root
project_folder = Path(__file__).resolve().parent.parent

# Complete student enquiry dataset
dataset_file = (
    project_folder
    / "data"
    / "student_enquiries"
    / "student_enquiries.csv"
)

# Save experimental results
output_file = (
    project_folder
    / "results"
    / "student_robustness_results.csv"
)


# --------------------------------------------------
# 2. Load the complete dataset
# --------------------------------------------------

with open(dataset_file, encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

assert len(rows) == 250, "Expected 250 student enquiries"

groups = defaultdict(list)

for row in rows:
    groups[(row["label"], row["source_topic"])].append(row)

labels = sorted(set(row["label"] for row in rows))

assert len(labels) == 5
assert len(groups) == 50
assert all(len(group) == 5 for group in groups.values())


# --------------------------------------------------
# 3. Create a topic-disjoint split
# --------------------------------------------------

def make_split(seed):
    rng = random.Random(seed)

    train_rows = []
    test_rows = []

    for label in labels:
        topics = sorted(
            topic for class_name, topic in groups
            if class_name == label
        )

        rng.shuffle(topics)

        for topic in topics[:8]:
            train_rows.extend(groups[(label, topic)])

        for topic in topics[8:]:
            test_rows.extend(groups[(label, topic)])

    rng.shuffle(train_rows)
    rng.shuffle(test_rows)

    train_topics = {
        (row["label"], row["source_topic"])
        for row in train_rows
    }

    test_topics = {
        (row["label"], row["source_topic"])
        for row in test_rows
    }

    assert train_topics.isdisjoint(test_topics)
    assert len(train_rows) == 200
    assert len(test_rows) == 50

    return train_rows, test_rows


# --------------------------------------------------
# 4. Gzip/NCD/kNN evaluation
# --------------------------------------------------

def evaluate_gzip(train_rows, test_rows):
    train_texts = [row["text"] for row in train_rows]
    train_labels = [row["label"] for row in train_rows]

    test_texts = [row["text"] for row in test_rows]
    test_labels = [row["label"] for row in test_rows]

    classifier = KnnExpText(
        agg_by_concat_space,
        DefaultCompressor("gzip"),
        NCD
    )

    classifier.calc_dis(
        test_texts,
        train_data=train_texts
    )

    predictions = []

    for distances in classifier.distance_matrix:
        nearest_indices = np.argsort(
            distances,
            kind="stable"
        )[:K]

        nearest_labels = [
            train_labels[i] for i in nearest_indices
        ]

        counts = Counter(nearest_labels)
        max_votes = max(counts.values())

        tied_labels = {
            label
            for label, count in counts.items()
            if count == max_votes
        }

        # Break ties using neighbour order, never the true label.
        prediction = next(
            label for label in nearest_labels
            if label in tied_labels
        )

        predictions.append(prediction)

    return accuracy_score(test_labels, predictions)


# --------------------------------------------------
# 5. TF-IDF + Logistic Regression evaluation
# --------------------------------------------------

def evaluate_baseline(train_rows, test_rows):
    train_texts = [row["text"] for row in train_rows]
    train_labels = [row["label"] for row in train_rows]

    test_texts = [row["text"] for row in test_rows]
    test_labels = [row["label"] for row in test_rows]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, train_labels)

    predictions = model.predict(X_test)

    return accuracy_score(test_labels, predictions)


# --------------------------------------------------
# 6. Run five experiments
# --------------------------------------------------

results = []

for seed in SEEDS:
    train_rows, test_rows = make_split(seed)

    gzip_accuracy = evaluate_gzip(train_rows, test_rows)
    baseline_accuracy = evaluate_baseline(train_rows, test_rows)

    results.append({
        "seed": seed,
        "gzip_accuracy": gzip_accuracy,
        "baseline_accuracy": baseline_accuracy
    })

    print(
        f"Seed {seed}: "
        f"Gzip={gzip_accuracy:.2%}, "
        f"TF-IDF+LR={baseline_accuracy:.2%}"
    )


# --------------------------------------------------
# 7. Calculate summary statistics
# --------------------------------------------------

gzip_scores = [row["gzip_accuracy"] for row in results]
baseline_scores = [row["baseline_accuracy"] for row in results]

print("\n=== ROBUSTNESS SUMMARY ===")

print(
    f"Gzip/NCD/kNN: "
    f"mean={statistics.mean(gzip_scores):.2%}, "
    f"SD={statistics.stdev(gzip_scores):.2%}"
)

print(
    f"TF-IDF + Logistic Regression: "
    f"mean={statistics.mean(baseline_scores):.2%}, "
    f"SD={statistics.stdev(baseline_scores):.2%}"
)

print(
    "Mean accuracy difference:",
    f"{statistics.mean(baseline_scores) - statistics.mean(gzip_scores):.2%}"
)


# --------------------------------------------------
# 8. Save results
# --------------------------------------------------

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["seed", "gzip_accuracy", "baseline_accuracy"]
    )

    writer.writeheader()
    writer.writerows(results)

print("\nResults saved to:", output_file)
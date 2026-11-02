import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# 1. Locate the student enquiry dataset
# --------------------------------------------------

data_folder = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "student_enquiries"
    / "classifier_dataset"
)


def load_data(filename):
    texts = []
    labels = []

    with open(filename, encoding="utf-8") as file:
        for line in file:
            label, text = line.rstrip("\n").split("\t", 1)
            labels.append(label)
            texts.append(text)

    return texts, labels


train_texts, train_labels = load_data(data_folder / "train.txt")
test_texts, test_labels = load_data(data_folder / "test.txt")

assert len(train_texts) == 200
assert len(test_texts) == 50

# --------------------------------------------------
# 2. Convert text into TF-IDF features
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

# --------------------------------------------------
# 3. Train Logistic Regression
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train, train_labels)

# --------------------------------------------------
# 4. Evaluate on the same test dataset
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(test_labels, predictions)

print("=== TF-IDF + LOGISTIC REGRESSION BASELINE ===")
print("Training examples:", len(train_texts))
print("Testing examples:", len(test_texts))
print(f"Accuracy: {accuracy:.2%}")

print("\nClassification report:")
print(
    classification_report(
        test_labels,
        predictions,
        zero_division=0,
        digits=3
    )
)

# --------------------------------------------------
# 5. Save predictions for reproducibility
# --------------------------------------------------

output_file = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "student_baseline_predictions.csv"
)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "true_label", "predicted_label"])

    for text, actual, predicted in zip(
        test_texts, test_labels, predictions
    ):
        writer.writerow([text, actual, predicted])

print("\nPredictions saved to:", output_file)
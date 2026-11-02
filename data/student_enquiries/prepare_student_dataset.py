import csv
import random
from collections import defaultdict
from pathlib import Path

folder_path = Path(__file__).resolve().parent
imput_file_path = folder_path / "student_enquiries.csv"
output_file_path = folder_path / "classifier_dataset"
output_file_path.mkdir(exist_ok=True)

with open(imput_file_path, encoding = "utf-8-sig") as file:
    rows = list(csv.DictReader(file))

# Group enquiries by their class and source topic
groups = defaultdict(list)

for row in rows:
    key = (row["label"], row["source_topic"])
    groups[key].append(row)

# Using a fixed random seed for reproducibility
rng = random.Random(42)

train_rows = []
test_rows = []

for label in sorted({row["label"] for row in rows}):
    topics = sorted(
        topic for class_name, topic in groups
        if class_name == label
    )
    rng.shuffle(topics)

    # 8 topics for training, two unseen topics for testing
    for topic in topics[:8]:
        train_rows.extend(groups[(label, topic)])

    for topic in topics[8:]:
        test_rows.extend(groups[(label, topic)])

rng.shuffle(train_rows)
rng.shuffle(test_rows)

# original classifier expects label TAB text
def save_txt(filename, data):
    with open(filename, "w", encoding = "utf-8") as file:
        for row in data:
            text = row["text"].replace("\t", " ").replace("\n", " ")
            file.write(f"{row['label']}\t{text}\n")

save_txt(output_file_path / "train.txt", train_rows)
save_txt(output_file_path / "test.txt", test_rows)

print("Training examples:", len(train_rows))
print("Testing examples:", len(test_rows))
print("Training topics:", len(set((r["label"], r["source_topic"]) for r in train_rows)))
print("Testing topics:", len(set((r["label"], r["source_topic"]) for r in test_rows)))

train_topics = {(r["label"], r["source_topic"]) for r in train_rows}
test_topics = {(r["label"], r["source_topic"]) for r in test_rows}

assert train_topics.isdisjoint(test_topics), "Topic leakage detected!"
print("Topic leakage check: PASSED")
print("Files saved in:", output_file_path)
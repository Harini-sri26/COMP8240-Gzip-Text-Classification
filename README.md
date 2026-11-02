# Gzip-Based Text Classification: Replication and Extension

**COMP8240 – Applications of Data Science | Macquarie University**

## Project Overview

This project replicates and extends the compression-based text classification approach presented in Jiang et al. (2023), *“Low-Resource” Text Classification: A Parameter-Free Classification Method with Compressors*.

The method uses gzip compression and Normalized Compression Distance (NCD) to measure similarities between texts, followed by k-nearest neighbours (kNN) classification. Unlike conventional supervised machine-learning methods, this approach does not require training a parameterised text representation model.

The project investigates the method's performance on a small subset of the AG News benchmark and a newly constructed synthetic student-enquiry dataset. It also compares compression-based classification with a TF-IDF and Logistic Regression baseline and examines the impact of tie-breaking rules on reported classification accuracy.

## Project Objectives

1. Replicate the original compression-based classification implementation on AG News.
2. Construct a new, balanced student-enquiry dataset for a university-support classification task.
3. Evaluate gzip/NCD/kNN on the new dataset.
4. Compare its performance against TF-IDF with Logistic Regression.
5. Investigate classification errors, robustness across different data splits, and evaluation methodology.

## Repository Structure

```text
COMP8240-Gzip-Text-Classification/
├── README.md
├── data/
│   └── student_enquiries/
│       ├── classifier_dataset/
│       │   ├── train.txt
│       │   └── test.txt
│       ├── create_student_enquiries.py
│       ├── prepare_student_dataset.py
│       ├── dataset_methodology.md
│       ├── raw_student_enquiries.csv
│       ├── source_topics.csv
│       └── student_enquiries.csv
├── original_codebase/
│   ├── compressors.py
│   ├── data.py
│   ├── experiments.py
│   ├── main_text.py
│   ├── utils.py
│   ├── ag_news_tie_comparison.py
│   ├── student_baseline.py
│   ├── student_error_analysis.py
│   ├── student_fair_evaluation.py
│   ├── student_performance_report.py
│   └── student_robustness.py
├── results/
│   ├── ag_news_replication/
│   └── [student-enquiry evaluation outputs]
└── report/
```

The `original_codebase/` directory contains code adapted from the original authors' implementation alongside additional evaluation scripts developed for this project. The student-enquiry scripts and AG News tie-comparison script are project extensions, not components of the original paper.

## New Dataset: Student Enquiries

A new dataset of **250 synthetic student enquiries** was constructed to investigate compression-based classification in a university-support setting.

The dataset contains five balanced categories:

| Category | Examples |
|---|---:|
| Enrolment | 50 |
| Fees | 50 |
| Assessment | 50 |
| Campus services | 50 |
| IT support | 50 |
| **Total** | **250** |

The dataset was developed using 50 source topics, with five enquiry phrasings per topic. The enquiries were generated with AI assistance and manually structured into labelled categories. Public university-support information informed topic selection; the examples are not records of real students.

The primary evaluation uses a topic-disjoint split:

- **Training:** 200 examples from 40 topics.
- **Testing:** 50 examples from 10 different topics.
- **Random seed:** 42.
- **Topic overlap:** None between training and testing.

This design reduces direct topic overlap between the training and testing sets, although related vocabulary and concepts can still appear across both sets.

Dataset construction details are documented in `data/student_enquiries/dataset_methodology.md`.

## Methodology

### Compression-Based Classification

For two texts, x and y, Normalized Compression Distance is calculated as:

NCD(x, y) = [C(xy) − min(C(x), C(y))] / max(C(x), C(y))

where C(x) is the compressed length of text x and C(xy) is the compressed length of their concatenation.

The implementation uses gzip compression and kNN classification.

### Baseline Model

A conventional machine-learning baseline was implemented using:

- TF-IDF word features with unigrams and bigrams.
- Logistic Regression.
- The same training and testing split as the compression-based classifier.

### Evaluation

The project examines classification accuracy, macro-averaged F1-score, per-class performance, confusion patterns and robustness across five topic-disjoint splits.

## Experimental Results

### AG News: Small-Scale Replication

The original implementation was evaluated using balanced subsets of AG News with gzip and k=2.

| Training examples | Testing examples | Original evaluation accuracy |
|---|---|---:|
| 40 | 20 | 50.00% |
| 200 | 80 | 58.75% |

These are small-scale implementation replications and should not be interpreted as reproductions of the paper's full benchmark results.

### AG News: Tie-Handling Investigation

Source-code inspection identified a ground-truth-dependent tie-resolution procedure in the original evaluation implementation.

A controlled comparison using the same 200 training examples, 80 testing examples, gzip/NCD distances, k=2, and nearest-neighbour ordering produced:

| Evaluation procedure | Accuracy |
|---|---:|
| Original tie handling | 58.75% |
| Label-independent tie handling | 46.25% |
| Difference | 12.50 percentage points |

There were 41 tied-vote cases, and the corrected procedure changed 10 predictions. All changed predictions occurred in tied-vote cases.

The label-independent procedure resolves tied class votes using the closest neighbour rather than consulting the test example's true label.

This finding applies to the evaluated implementation and sample; it does not establish the size of any effect on the published paper's full benchmark results.

### Student-Enquiry Dataset

| Model | Accuracy | Macro F1-score |
|---|---:|---:|
| gzip/NCD/kNN, k=5 | 64.00% | 0.644 |
| TF-IDF + Logistic Regression | 82.00% | 0.818 |

The k=5 compression-based result was the highest among the tested k values of 1, 2, 3 and 5 on the test set. Because k was selected using test-set performance, this result should be interpreted as exploratory rather than as an unbiased estimate after hyperparameter tuning.

### Robustness Across Five Splits

| Model | Mean accuracy | Standard deviation |
|---|---:|---:|
| gzip/NCD/kNN | 64.00% | 9.70 percentage points |
| TF-IDF + Logistic Regression | 83.20% | 7.29 percentage points |

The TF-IDF baseline outperformed the compression-based method across all five evaluated splits. These splits reuse the same underlying dataset and should not be treated as five independent datasets.

## Running the Project

Run commands from the repository root in a Python environment with the required dependencies installed.

### Student-Enquiry Experiments

```bash
python original_codebase/student_fair_evaluation.py
python original_codebase/student_baseline.py
python original_codebase/student_performance_report.py
python original_codebase/student_error_analysis.py
python original_codebase/student_robustness.py
```

### AG News Replication

The AG News experiments require the TorchText AG News dataset and the dependencies used by the original implementation.

```bash
python original_codebase/main_text.py \
  --dataset AG_NEWS \
  --data_dir data \
  --num_train 50 \
  --num_test 20 \
  --compressor gzip \
  --k 2 \
  --output_dir results/ag_news_replication
```

**Reproducibility note:** The original sampling procedure does not set a fixed random seed internally. Running the command above may select different examples. Saved `.npy` index files record the samples used for the reported experiments.

### AG News Tie Comparison

```bash
python original_codebase/ag_news_tie_comparison.py
```

This script reconstructs the saved AG News samples, calculates the original gzip/NCD distances, and compares the original and label-independent evaluation procedures.

## Ethics and Limitations

- **Synthetic data:** The student enquiries are AI-assisted synthetic examples, not authentic student-support records.
- **Privacy:** No real student identities or private enquiry records were intentionally included.
- **Representativeness:** The dataset is small, balanced and manually structured, so it may not reflect real enquiry frequencies, language diversity, ambiguity or complexity.
- **Labelling assumptions:** Categories and topic assignments were defined during dataset construction rather than established through independent annotator agreement.
- **Evaluation limitations:** Small test sets, exploratory k selection and overlapping repeated splits limit generalisability.
- **Practical risks:** Misclassification of enquiries about fees, enrolment or assessments could lead to incorrect guidance or delayed support. Human review would be required before considering practical deployment.

## Original Work and Attribution

This project is based on:

Jiang et al. (2023). *“Low-Resource” Text Classification: A Parameter-Free Classification Method with Compressors*. Findings of ACL 2023.

The original compression-based classification framework was developed by the paper's authors. This repository includes adapted original implementation files and separately developed student-dataset generation, baseline, evaluation, robustness and tie-handling analysis scripts.

The original paper and code repository should be consulted for the full benchmark methodology, implementation details and applicable reuse terms.

Paper: https://aclanthology.org/2023.findings-acl.426/
Original software: npc-gzip, published on PyPI at https://pypi.org/project/npc-gzip/
Original code licence: MIT License, copyright © 2023 Gin Jiang.

The original implementation files are reused under the MIT License, with the original copyright and permission notice retained in LICENSE. Dataset construction, baseline modelling, robustness evaluation and tie-handling analysis are extensions undertaken for this academic project.

## Academic Context

This repository was developed as part of the COMP8240 Applications of Data Science assessment at Macquarie University. It is an academic replication and extension project, not a production-ready student-support classification system.

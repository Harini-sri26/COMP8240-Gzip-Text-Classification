# Student Enquiry Dataset — Construction Methodology

## 1. Dataset objective

This dataset was constructed to evaluate whether a compression-based text classifier using gzip, Normalized Compression Distance (NCD), and k-nearest neighbours (kNN) can categorise short university student enquiries.

## 2. Data source and construction

The dataset consists of **250 synthetic student enquiries** across five categories:

| Category | Enquiries |
|---|---:|
| Enrolment | 50 |
| Fees | 50 |
| Assessment | 50 |
| Campus Services | 50 |
| IT Support | 50 |
| **Total** | **250** |

Fifty source topics were selected to reflect common university administrative and student-support needs, informed by publicly available university support and FAQ information. The topics and their associated reference URLs are recorded in `source_topics.csv`.

Five differently worded enquiries were drafted for each topic, with AI assistance. The resulting examples are synthetic and do not represent actual enquiries collected from students.

## 3. Annotation

Each enquiry was assigned one of five predefined category labels during construction.

The labels represent the primary purpose of the enquiry rather than individual keywords. For example, a question about whether fees remain payable after withdrawing from a unit is labelled `fees`, whereas a question about the withdrawal process is labelled `enrolment`.

These are construction-time labels, not independently annotated ground-truth labels. Some examples may be ambiguous across categories.

## 4. Preprocessing and quality checks

The constructed enquiries were manually reviewed for spelling and formatting errors.

Structural validation confirmed:

- 250 enquiries in total.
- Five balanced categories containing 50 enquiries each.
- Fifty source topics, each represented by five enquiries.
- No duplicate enquiry texts.
- No missing required fields.
- Sequential enquiry identifiers.

The corrected dataset was saved as `student_enquiries.csv`.

## 5. Training and testing split

A reproducible topic-disjoint split was created using a fixed random seed of 42.

Within each category, eight topics were allocated to training and two to testing. All five enquiries associated with a topic remained in the same split.

This produced:

- **Training:** 200 enquiries across 40 topics.
- **Testing:** 50 enquiries across 10 previously unseen topics.

The topic-disjoint approach reduces the risk of closely related paraphrases appearing in both training and testing.

## 6. Classification method

The dataset was evaluated using the original gzip/NCD/kNN implementation.

Experiments were conducted using k values of 1, 2, 3 and 5.

A separate evaluation script was also developed to calculate predictions without using the true test labels to resolve voting ties, addressing a limitation identified in the original implementation.

## 7. Limitations

The dataset is small, synthetic and balanced by design. Consequently, it may not reflect the language variation, class frequencies, spelling errors or ambiguity found in real student enquiries.

The category labels were assigned during construction rather than independently annotated by multiple reviewers.

The experiments use a single topic-disjoint train/test split. Results may vary under different splits or with independently collected enquiries.

The k-value comparisons are exploratory and should not be interpreted as unbiased model selection or definitive estimates of real-world performance.

## 8. Error analysis and annotation review

The label-independent evaluation achieved 64% accuracy (32/50 correct) with k=5, with a macro F1-score of 0.644.

All 18 misclassified enquiries were reviewed to investigate classification errors and potential label ambiguity.

Three key observations emerged:

1. **Overlapping vocabulary:** All three misclassified Fees enquiries were predicted as Enrolment and concerned fee refunds following withdrawal. This illustrates the difficulty of distinguishing primary intent when categories share terminology.
2. **Short-text classification:** Several brief enquiries about campus locations, assessment results and technical assistance were assigned incorrect categories. Limited textual context may contribute to these errors.
3. **Generalisation to unseen topics:** The topic-disjoint evaluation tests enquiries from topics absent from training, but additional experiments would be required to isolate the effect of topic novelty.

No obvious construction-time label errors were identified among the 18 reviewed misclassifications. The labels were therefore retained without modification.

The review does not establish full-dataset annotation reliability. Future work could include independent annotation, inter-annotator agreement, larger datasets, repeated topic-disjoint splits and comparison against baseline classifiers.

The observed 64% accuracy is exploratory because k=5 was selected after comparing multiple values on the same test set.

## 9. Baseline comparison and robustness evaluation

A conventional TF-IDF (word unigrams and bigrams) with Logistic Regression classifier was evaluated against gzip/NCD/kNN using identical training and testing examples.

On the initial topic-disjoint split (seed 42), gzip/NCD/kNN with k=5 achieved 64% accuracy and a macro F1-score of 0.644. TF-IDF with Logistic Regression achieved 82% accuracy and a macro F1-score of 0.818.

To examine sensitivity to the train/test partition, five topic-disjoint splits were evaluated using seeds 42, 123, 2026, 7 and 99. Each split contained 200 training enquiries and 50 testing enquiries, with no shared source topics between training and testing.

Across these splits:

- gzip/NCD/kNN (k=5): mean accuracy 64.0%, sample standard deviation 9.70 percentage points.
- TF-IDF + Logistic Regression: mean accuracy 83.2%, sample standard deviation 7.29 percentage points.
- Mean paired accuracy difference: 19.2 percentage points in favour of TF-IDF + Logistic Regression.

The baseline outperformed gzip/NCD/kNN on all five evaluated splits. These findings suggest that the conventional word-feature baseline is more effective on this particular synthetic student-enquiry dataset under the tested configurations.

However, the evaluation remains exploratory. The dataset is small and synthetic, repeated splits are not statistically independent, and k=5 was selected following initial test-set exploration. Further evaluation on independent real-world enquiries would be required to establish generalisability.
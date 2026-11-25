---
name: abstain-qa-eval
description: Evaluates large language models' ability to abstain from answering when questions are unanswerable or when uncertain, while maintaining accuracy on answerable questions. It measures how well models balance abstention with correct answer selection under different prompting strategies and uncertainty calibration methods. Use when the user wants to benchmark on Abstain-QA, or asks about evaluating this task. Reports Abstention Rate (AR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.16221
  bibtex_key: firstauthor2024abstention
  confidence: high
---

# abstain-qa-eval

> Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large Language Models — First Author et al. (2024) (arXiv:2407.16221, 2024)

## What this evaluates

Evaluates large language models' ability to abstain from answering when questions are unanswerable or when uncertain, while maintaining accuracy on answerable questions. It measures how well models balance abstention with correct answer selection under different prompting strategies and uncertainty calibration methods.

## Datasets

- **Abstain-QA** — total ?; splits: test (-1)

## Metrics

- `Abstention Rate (AR)` **(primary)** — range: [0, 1]
  - AR = (FN + TN) / |D|, where FN is false negatives (abstaining on answerable questions), TN is true negatives (correctly abstaining on unanswerable questions), and |D| is the total number of QA pairs in the dataset.
- `Answerable Accuracy (AAC)` — range: [0, 1]
  - AAC = TP / |A|, where TP is true positives (correctly selecting a candidate option on answerable questions) and |A| is the number of answerable QAs.
- `Unanswerable Accuracy (UAC)` — range: [0, 1]
  - UAC = TN / |U|, where TN is true negatives (correctly abstaining on unanswerable questions) and |U| is the number of unanswerable QAs.
- `Precision (P)` — range: [0, 1]
  - P = TP / (TP + FP), measuring the reliability of the model's non-abstention predictions.

## Input / output format

**Input**: Task Prompt ($\phi$) containing the multiple-choice question, options, and output formatting requirements, combined with an Abstain Clause ($\alpha$) that varies in sensitivity to uncertainty (Standard, Abstain, or Extreme Abstain).

**Output**: A single selected option from the provided choices, or an abstention option (IDK/NOTA). In the Verbal Confidence experiment, a confidence score from 1 to 5 is also required.

## Scoring recipe

```python
TP, FP, TN, FN = 0, 0, 0, 0
n_answerable, n_unanswerable = 0, 0
for sample in dataset:
    is_answerable = (sample.gt != 'IDK/NOTA')
    pred = model.predict(sample.prompt, sample.abstain_clause)
    if confidence_thresholding and sample.conf <= threshold:
        pred = 'IDK/NOTA'
    if is_answerable:
        n_answerable += 1
        if pred == sample.gt: TP += 1
        elif pred == 'IDK/NOTA': FN += 1
        else: FP += 1
    else:
        n_unanswerable += 1
        if pred == 'IDK/NOTA': TN += 1
        else: FP += 1
AR = (FN + TN) / len(dataset)
AAC = TP / n_answerable
UAC = TN / n_unanswerable
P = TP / (TP + FP)
```

## Common pitfalls

- Misclassifying failure to abstain on unanswerable questions as False Negatives instead of False Positives, which distorts the confusion matrix.
- Ignoring the confidence thresholding step in the Verbal Confidence experiment, where low-confidence predictions are forcibly converted to abstentions before metric calculation.
- Assuming a higher Abstention Rate (AR) inherently indicates better model quality; the protocol explicitly aims to maximize UAC and Precision while minimizing FN to preserve AAC.

## Evidence (verbatim from paper)

> To quantify how often a model abstains, we define a new metric, called Abstention Rate (AR): AR = (FN+TN)/|D| where |D| is the number of QAs in the dataset. Moreover, we define the Answerable Accuracy, AAC, measuring the accuracy of correct option selection in answerable QAs and Unanswerable Accuracy, UAC, measuring the accuracy of abstention in unanswerable QA: AAC = TP/|A|, UAC = TN/|U| where |A| is the number of answerable QAs and |U| is the number of unanswerable QAs. We also use P = TP/(TP+FP) in our evaluations.

## Citation

```bibtex
@misc{firstauthor2024abstention,
  title={Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large Language Models},
  author={First Author et al. (2024)},
  year={2024},
  note={arXiv:2407.16221}
}
```

- arXiv: 2407.16221

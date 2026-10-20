---
name: 2m-belebele-eval
description: Multilingual reading comprehension across text and speech modalities. It probes a model's ability to understand spoken or written passages in 39 languages and answer multiple-choice questions based on them. Use when the user wants to benchmark on 2M-Belebele, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.08274
  bibtex_key: costajussa20242mbelebele
  confidence: high
---

# 2m-belebele-eval

> 2M-BELEBELE: Highly Multilingual Speech and American Sign Language Comprehension Dataset — Costa-jussà et al. (2024) (arXiv:2412.08274, 2024)

## What this evaluates

Multilingual reading comprehension across text and speech modalities. It probes a model's ability to understand spoken or written passages in 39 languages and answer multiple-choice questions based on them.

## Datasets

- **2M-Belebele** — total ?; splits: test (-1); repo https://github.com/facebookresearch/belebele

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Proportion of correctly predicted answer letters out of total instances. Reported as the average over 3 independent runs with random seeds 0, 1, and 2.
- `% ≥ 50` — range: [0, 1]
  - Proportion of languages for which a given model's accuracy exceeds 50%.
- `% ≥ 70` — range: [0, 1]
  - Proportion of languages for which a given model's accuracy exceeds 70%.

## Input / output format

**Input**: A passage (text or audio), a multiple-choice question, and four answer options (A, B, C, D). For 5-shot evaluation, the input also includes randomly sampled English training examples formatted as text.

**Output**: A single uppercase letter (A, B, C, or D) corresponding to the correct answer, with no additional text or explanation.

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p == g)
    return correct / len(golds)

# Extract predicted letter from model output
pred_letters = [extract_first_letter(out) for out in model_outputs]
# Average over 3 runs
acc_runs = [compute_accuracy(pred_letters_run, gold_letters) for run in range(3)]
final_accuracy = sum(acc_runs) / 3
```

## Common pitfalls

- Do not select the answer with the highest probability; directly assess the predicted letter of the answer.
- Few-shot examples are provided in text format, which can cause modality mismatch if the test passage is in speech.
- Results must be averaged over 3 runs (seeds 0, 1, 2); single-run results may vary significantly.

## Evidence (verbatim from paper)

> For 5-shot and zero-shot settings, our instruction prompt is as follows “Given the following passage, query, and answer choices, output the letter corresponding to the correct answer. Do not write any explanation. Only output the letter within A, B, C, or D that corresponds to the correct answer.” and we report the averaged accuracy over 3 runs333Random seeds: 0, 1, 2.. Different from Bandarkar et al. ([2023]), we do not pick the answer with the highest probability but directly assess the predicted letter of the answer.

## Citation

```bibtex
@misc{costajussa20242mbelebele,
  title={2M-BELEBELE: Highly Multilingual Speech and American Sign Language Comprehension Dataset},
  author={Costa-jussà et al. (2024)},
  year={2024},
  note={arXiv:2412.08274}
}
```

- arXiv: 2412.08274

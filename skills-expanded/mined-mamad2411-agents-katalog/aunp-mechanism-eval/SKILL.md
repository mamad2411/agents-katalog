---
name: aunp-mechanism-eval
description: Evaluates whether large language models can correctly reason about physicochemical mechanisms in gold nanoparticle synthesis using multiple-choice questions. It probes both factual recall and the depth of mechanistic understanding by measuring prediction accuracy and model confidence derived from output logits. Use when the user wants to benchmark on AuNP Synthesis Mechanism Benchmark, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.08922
  bibtex_key: pu2024leveraging
  confidence: high
---

# aunp-mechanism-eval

> Leveraging large language models for nano synthesis mechanism explanation: solid foundations or mere conjectures? — Pu et al. (2024) (arXiv:2407.08922, 2024)

## What this evaluates

Evaluates whether large language models can correctly reason about physicochemical mechanisms in gold nanoparticle synthesis using multiple-choice questions. It probes both factual recall and the depth of mechanistic understanding by measuring prediction accuracy and model confidence derived from output logits.

## Datasets

- **AuNP Synthesis Mechanism Benchmark** — total 775; splits: test (775)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Binary score: 1 if the model's selected option matches the gold answer, 0 otherwise. Averaged across all N questions.
- `c-score` — range: [0, 1]
  - Confidence-based score computed from pre-Softmax logits for the four options (A, B, C, D). Formula: (1/N) * sum(exp(L_G) / (exp(L_A) + exp(L_B) + exp(L_C) + exp(L_D))) for each question, where L_G is the gold option's logit.

## Input / output format

**Input**: Multiple-choice question containing a scenario, options (A, B, C, D), and instructions. Evaluated across temperature settings (0.1, 0.3, 0.5, 0.7, 0.9).

**Output**: Model selects one option from the predefined vocabulary {A, B, C, D}. Pre-Softmax logits for all four options are recorded for c-score calculation.

## Scoring recipe

```python
def evaluate(predictions, golds, logits, N):
    accuracy = sum(1 for p, g in zip(predictions, golds) if p == g) / N
    c_scores = []
    for i in range(N):
        l_a, l_b, l_c, l_g = logits[i]['A'], logits[i]['B'], logits[i]['C'], logits[i][golds[i]]
        c_scores.append(math.exp(l_g) / (math.exp(l_a) + math.exp(l_b) + math.exp(l_c) + math.exp(l_g)))
    c_score = sum(c_scores) / N
    return accuracy, c_score
```

## Common pitfalls

- Temperature settings significantly alter both accuracy and c-score; lower temperatures generally yield higher confidence but may reduce accuracy if the model becomes overconfident in wrong answers.
- c-score can diverge from accuracy, revealing cases where models guess correctly with low confidence or incorrectly with high confidence, which pure accuracy masks.
- Models may rely on keyword matching rather than true physicochemical reasoning, leading to inflated accuracy on superficially similar questions.

## Evidence (verbatim from paper)

> In order to obtain the binary accuracy of the model, for each multiple-choice questions, one point will be given to the model if it selected the gold answer, otherwise zero. This process will also be repeated with different temperature settings, i.e., from 0.1 to 0.9 with 5 steps. Finally, the average score of each model will be ranked. ... We here evaluate the overall confidence using the formulated c-score, which quantifies the confidence level assigned to each correct answer, as detailed in the E.q. [1]: c-score = (1/N) sum_{i=1}^{N} e^{L_G^i} / (e^{L_A^i} + e^{L_B^i} + e^{L_C^i} + e^{L_D^i})

## Citation

```bibtex
@misc{pu2024leveraging,
  title={Leveraging large language models for nano synthesis mechanism explanation: solid foundations or mere conjectures?},
  author={Pu et al. (2024)},
  year={2024},
  note={arXiv:2407.08922}
}
```

- arXiv: 2407.08922

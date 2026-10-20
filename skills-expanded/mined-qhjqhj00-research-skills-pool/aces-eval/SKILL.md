---
name: aces-eval
description: Evaluates machine translation metrics on their ability to correctly rank good translations above incorrect ones across specific linguistic error phenomena. It probes metric robustness to fine-grained translation errors like hallucination, omission, and real-world knowledge failures. Use when the user wants to benchmark on ACES, or asks about evaluating this task. Reports Kendall's tau-like correlation.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.01153
  bibtex_key: amrhein2023aces
  confidence: high
---

# aces-eval

> ACES: Translation Accuracy Challenge Sets at WMT 2023 — Amrhein et al. (2023) (arXiv:2311.01153, 2023)

## What this evaluates

Evaluates machine translation metrics on their ability to correctly rank good translations above incorrect ones across specific linguistic error phenomena. It probes metric robustness to fine-grained translation errors like hallucination, omission, and real-world knowledge failures.

## Datasets

- **ACES** — total 36476; splits: test (36476); repo https://github.com/EdinburghNLP/ACES

## Metrics

- `Kendall's tau-like correlation` **(primary)** — range: [-1, 1]
  - Measures the proportion of correctly ranked pairs minus incorrectly ranked pairs: τ = (concordant - discordant) / (concordant + discordant), where concordant means the metric scores the good translation higher than the incorrect one, and discordant means it scores it equal to or lower.

## Input / output format

**Input**: Per instance: source sentence, reference translation, a 'good' system translation, and an 'incorrect' system translation.

**Output**: A scalar score assigned by the evaluated metric to the translation pair, used to determine concordance/discordance.

## Scoring recipe

```python
def compute_tau(good_scores, bad_scores):
    concordant = sum(1 for g, b in zip(good_scores, bad_scores) if g > b)
    discordant = sum(1 for g, b in zip(good_scores, bad_scores) if g <= b)
    return (concordant - discordant) / (concordant + discordant)
```

## Common pitfalls

- Do not draw conclusions based solely on the aggregate ACES-Score; the paper explicitly warns that performance varies highly across error categories.
- Assume reference-based metrics will consistently outperform reference-free ones; the evaluation shows reference-free metrics often perform on par or better.
- Ignore fine-grained sub-categories (e.g., hallucination vs. discourse) within the mistranslation category, as performance is highly variable and LLM-based metrics struggle specifically with hallucination.

## Evidence (verbatim from paper)

> We first compute the Kendall's tau-like correlation scores (Freitag et al., 2021, 2022) for all of the ACES examples. This metric measures the number of times a metric scores the good translation above the incorrect translation (concordant) and equal to or lower than the incorrect translation (discordant): $$ \tau = \frac {\text {c o n c o r d a n t} - \text {d i s c o r d a n t}}{\text {c o n c o r d a n t} + \text {d i s c o r d a n t}} $$

## Citation

```bibtex
@misc{amrhein2023aces,
  title={ACES: Translation Accuracy Challenge Sets at WMT 2023},
  author={Amrhein et al. (2023)},
  year={2023},
  note={arXiv:2311.01153}
}
```

- arXiv: 2311.01153

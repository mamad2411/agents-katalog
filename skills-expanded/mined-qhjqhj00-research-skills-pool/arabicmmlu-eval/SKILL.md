---
name: arabicmmlu-eval
description: ArabicMMLU probes massive multitask language understanding in Modern Standard Arabic across 40 educational subjects spanning STEM, social sciences, humanities, Arabic language, and culturally specific domains. It evaluates models on cross-lingual transfer, cultural localization, and robustness to linguistic phenomena like negation across primary, middle, high school, and university levels. The benchmark specifically tests how well models handle Arabic-specific knowledge and exam-style multiple-choice questions. Use when the user wants to benchmark on ArabicMMLU, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.12840
  bibtex_key: koto2024arabicmmlu
  confidence: high
---

# arabicmmlu-eval

> ArabicMMLU: Assessing Massive Multitask Language Understanding in Arabic — Koto et al. (2024) (arXiv:2402.12840, 2024)

## What this evaluates

ArabicMMLU probes massive multitask language understanding in Modern Standard Arabic across 40 educational subjects spanning STEM, social sciences, humanities, Arabic language, and culturally specific domains. It evaluates models on cross-lingual transfer, cultural localization, and robustness to linguistic phenomena like negation across primary, middle, high school, and university levels. The benchmark specifically tests how well models handle Arabic-specific knowledge and exam-style multiple-choice questions.

## Datasets

- **ArabicMMLU** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly answered questions. For open-source models, the predicted option is the one with the highest probability among the five candidate tokens (A, B, C, D, E or their Arabic equivalents). For closed-source models, the answer is extracted via regex from the first generated token; if no match occurs, a random option is assigned.

## Input / output format

**Input**: Multiple-choice question presented in Arabic or English, accompanied by five options (A–E) in Arabic or English alphabetic script. Prompt templates may vary by language and output script.

**Output**: A single alphabetic character (A, B, C, D, or E) corresponding to the selected option.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Prompt language and output script choice drastically impacts scores; English prompts with English alphabetic outputs consistently yield the highest accuracy across most models, contrary to expectations for an Arabic benchmark.
- Closed-source API models rely on regex matching the very first generated token, which frequently fails and requires a random fallback, potentially introducing noise if not explicitly handled.
- Few-shot prompting improves base models but degrades instruction-tuned models, so evaluation settings must be carefully matched to model type to avoid misleading comparisons.

## Evidence (verbatim from paper)

> Table 4: Zero-shot LLM performance (% accuracy), combined across subject groups. Following previous studies, for open-source models, we determine the answer based on the highest probability among all possible options. In the case of English alphabetic output, we measure the probability of the first generated token being A, B, C, D, or E. For Arabic, we measure the probability of the first generated token being <أ>, <ب>, <ج>, <د>, or <ه>. For closed-source models, we determine the answer based on the first token generated in the text using a regular expression. If there is no match, we assign a random answer.

## Citation

```bibtex
@misc{koto2024arabicmmlu,
  title={ArabicMMLU: Assessing Massive Multitask Language Understanding in Arabic},
  author={Koto et al. (2024)},
  year={2024},
  note={arXiv:2402.12840}
}
```

- arXiv: 2402.12840

---
name: art-audio-reasoning-eval
description: This benchmark evaluates multimodal large language models on their ability to perform cross-modal audio reasoning. It requires models to integrate multiple audio cues (e.g., speech, environmental sounds, speaker identity) and apply logical inference to answer questions, rather than just performing isolated audio tasks like transcription or classification. Use when the user wants to benchmark on ART (Audio Reasoning Tasks), or asks about evaluating this task. Reports Absolute accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.19673
  bibtex_key: christop2026art
  confidence: high
---

# art-audio-reasoning-eval

> A Benchmark for Audio Reasoning Capabilities of Multimodal Large Language Models — Christop et al. (2026) (arXiv:2601.19673, 2026)

## What this evaluates

This benchmark evaluates multimodal large language models on their ability to perform cross-modal audio reasoning. It requires models to integrate multiple audio cues (e.g., speech, environmental sounds, speaker identity) and apply logical inference to answer questions, rather than just performing isolated audio tasks like transcription or classification.

## Datasets

- **ART (Audio Reasoning Tasks)** — total ?; splits: test (-1)

## Metrics

- `Absolute accuracy` **(primary)** — range: [0, 1]
  - Calculated as the number of correct answers divided by the total number of evaluated instances. For the Yes/No approach, inference is run five times and results are averaged.
- `Relative accuracy` — range: [0, 1]
  - Accuracy calculated only on relevant responses (i.e., where the model strictly output 'Yes' or 'No'). Irrelevant responses are excluded from the denominator.

## Input / output format

**Input**: An audio prompt containing multiple modalities (e.g., speech, environmental sounds, speaker cues) paired with a natural language question requiring logical inference or cross-modal deduction.

**Output**: For the primary evaluation: a strict binary response ('Yes' or 'No'). An alternative descriptive open-ended response is also evaluated using LLM-as-a-judge.

## Scoring recipe

```python
def score_yes_no(predictions, gold_answers):
    relevant_count = 0
    correct_count = 0
    for pred, gold in zip(predictions, gold_answers):
        if pred.strip().lower() in ['yes', 'no']:
            relevant_count += 1
            if pred.strip().lower() == gold.strip().lower():
                correct_count += 1
    return correct_count / relevant_count if relevant_count > 0 else 0.0
```

## Common pitfalls

- Models frequently fail to adhere to the strict Yes/No constraint, outputting descriptive text instead. This lowers the relevant response rate and artificially deflates accuracy if not filtered out.
- Task confusion is common: models often default to transcription or speaker identification rather than performing the required logical inference, leading to systematic failures.
- LLM-as-a-judge evaluation exhibits strong self-bias and same-family bias, where models like Qwen3 rate their own outputs or sibling models significantly higher than independent judges.

## Evidence (verbatim from paper)

> The relative accuracy is defined as the accuracy calculated only on relevant responses. In this case, the models were instructed to answer only Yes or No. The inference on each of the models was run five times and the results were averaged to assess whether the models exhibit superiority over random guessing.

## Citation

```bibtex
@misc{christop2026art,
  title={A Benchmark for Audio Reasoning Capabilities of Multimodal Large Language Models},
  author={Christop et al. (2026)},
  year={2026},
  note={arXiv:2601.19673}
}
```

- arXiv: 2601.19673

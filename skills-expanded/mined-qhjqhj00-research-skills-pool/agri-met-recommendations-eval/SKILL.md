---
name: agri-met-recommendations-eval
description: Evaluates the ability of LLMs to generate accurate and context-aware agricultural recommendations (sowing schedules, irrigation plans, risk mitigation) based on integrated weather, soil, and crop data. It specifically probes how multi-round prompt engineering improves recommendation quality compared to single-round and Chain-of-Thought baselines. Use when the user wants to benchmark on Agricultural Meteorological Dataset, or asks about evaluating this task. Reports Accuracy (Acc).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2408.04640
  bibtex_key: park2024llms
  confidence: medium
---

# agri-met-recommendations-eval

> LLMs for Enhanced Agricultural Meteorological Recommendations — Park et al. (2024) (arXiv:2408.04640, 2024)

## What this evaluates

Evaluates the ability of LLMs to generate accurate and context-aware agricultural recommendations (sowing schedules, irrigation plans, risk mitigation) based on integrated weather, soil, and crop data. It specifically probes how multi-round prompt engineering improves recommendation quality compared to single-round and Chain-of-Thought baselines.

## Datasets

- **Agricultural Meteorological Dataset** — total ?; splits: test (-1)

## Metrics

- `Accuracy (Acc)` **(primary)** — range: percent
  - Calculates the percentage of generated recommendations that exactly match the ground truth dataset.
- `GPT-4 Score` — range: [1, 5]
  - LLM-as-a-judge metric where GPT-4 rates each recommendation on clarity, specificity, and practicality on a numerical scale (observed range 1-5 in results).

## Input / output format

**Input**: 10-day weather forecasts (temperature, precipitation, wind), soil conditions (moisture, nutrients, pH), crop data (type, growth stage, requirements), and historical yield/planting dates.

**Output**: Agricultural recommendations including sowing schedules, irrigation plans, and risk mitigation strategies.

## Scoring recipe

```python
# Accuracy
correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)
acc = (correct / len(predictions)) * 100

# GPT-4 Score
scores = []
for p in predictions:
    prompt = f"Rate recommendation on clarity, specificity, practicality (1-5): {p}"
    scores.append(extract_number(call_gpt4(prompt)))
gpt4_score = sum(scores) / len(scores)
```

## Common pitfalls

- Ground truth definition for Accuracy is unspecified (e.g., expert consensus vs. historical best practice), making exact match evaluation ambiguous.
- GPT-4 scoring prompt and exact rating scale are not fully detailed, risking judge bias or inconsistency across runs.
- Dataset size and train/test splits are omitted, preventing statistical validation or generalization assessment.

## Evidence (verbatim from paper)

> We utilized two primary evaluation metrics to assess the performance of our method: Accuracy (Acc) and GPT-4 scoring. Accuracy measures the correctness of the recommendations by comparing them to a ground truth dataset. The GPT-4 scoring metric evaluates the quality and relevance of the generated recommendations, where the outputs are rated by GPT-4 based on predefined criteria such as clarity, specificity, and practicality.

## Citation

```bibtex
@misc{park2024llms,
  title={LLMs for Enhanced Agricultural Meteorological Recommendations},
  author={Park et al. (2024)},
  year={2024},
  note={arXiv:2408.04640}
}
```

- arXiv: 2408.04640

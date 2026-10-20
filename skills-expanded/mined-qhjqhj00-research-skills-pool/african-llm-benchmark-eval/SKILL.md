---
name: african-llm-benchmark-eval
description: This evaluation probes the cross-lingual reasoning and domain knowledge capabilities of large language models across low-resource African languages. It measures how well models perform on translated benchmarks compared to English, and assesses the impact of cultural appropriateness and fine-tuning data quality on model accuracy. Use when the user wants to benchmark on Winogrande, MMLU (Clinical Sections), Belebele, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.12417
  bibtex_key: alhanai2024bridging
  confidence: high
---

# african-llm-benchmark-eval

> Bridging the Gap: Enhancing LLM Performance for Low-Resource African Languages with New Benchmarks, Fine-Tuning, and Cultural Adjustments — Alhanai et al. (2024) (arXiv:2412.12417, 2024)

## What this evaluates

This evaluation probes the cross-lingual reasoning and domain knowledge capabilities of large language models across low-resource African languages. It measures how well models perform on translated benchmarks compared to English, and assesses the impact of cultural appropriateness and fine-tuning data quality on model accuracy.

## Datasets

- **Winogrande** — total ?; splits: test (-1); repo https://github.com/InstituteforDiseaseModeling/Bridging-the-Gap-Low-Resource-African-Languages
- **MMLU (Clinical Sections)** — total ?; splits: test (-1); repo https://github.com/InstituteforDiseaseModeling/Bridging-the-Gap-Low-Resource-African-Languages
- **Belebele** — total ?; splits: test (-1); repo https://github.com/InstituteforDiseaseModeling/Bridging-the-Gap-Low-Resource-African-Languages

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly predicted answer choices out of the total number of instances. Calculated as (correct predictions / total predictions) * 100.

## Input / output format

**Input**: Multiple-choice questions (binary choice for Winogrande, 5-option for MMLU/Belebele) presented in target African languages or English. Winogrande and MMLU use a 5-shot prompt format; Belebele uses a 0-shot format.

**Output**: The model's selected answer option (e.g., 'A', 'B', or the full text of the chosen option).

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p.strip().upper() == g.strip().upper())
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Shot configuration varies by benchmark: Winogrande and MMLU require 5-shot prompting, while Belebele uses 0-shot.
- Cultural appropriateness annotations significantly split the dataset; performance lifts are reported only on QA pairs deemed culturally appropriate by native speakers.
- Machine-translated queries sometimes yield comparable performance to native-language models, which can mask true cross-lingual gaps if not explicitly controlled.

## Evidence (verbatim from paper)

> The average 5-shot (0-shot for Belebele) accuracy scores across all languages and benchmarks are reported in Table [1], with English for reference.

## Citation

```bibtex
@misc{alhanai2024bridging,
  title={Bridging the Gap: Enhancing LLM Performance for Low-Resource African Languages with New Benchmarks, Fine-Tuning, and Cultural Adjustments},
  author={Alhanai et al. (2024)},
  year={2024},
  note={arXiv:2412.12417}
}
```

- arXiv: 2412.12417

---
name: arabculture-eval
description: Evaluates large language models' ability to perform commonsense reasoning within specific Arab cultural contexts. It probes region-specific grounding by testing models across 13 Arab countries and 12 cultural domains, measuring how well they understand local norms, habits, and social scenarios in both Arabic and English. Use when the user wants to benchmark on ArabCulture, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2502.12788
  bibtex_key: sadallah2025commonsense
  confidence: high
---

# arabculture-eval

> Commonsense Reasoning in Arab Culture — Sadallah et al. (2025) (arXiv:2502.12788, 2025)

## What this evaluates

Evaluates large language models' ability to perform commonsense reasoning within specific Arab cultural contexts. It probes region-specific grounding by testing models across 13 Arab countries and 12 cultural domains, measuring how well they understand local norms, habits, and social scenarios in both Arabic and English.

## Datasets

- **ArabCulture** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Calculated as the percentage of correctly predicted answers out of the total number of instances. For MCQ, it measures the proportion of times the model selects the ground-truth option. For sentence completion, it measures the proportion of times the model assigns the highest likelihood to the correct continuation.

## Input / output format

**Input**: A prompt containing a premise followed by multiple-choice options (labeled A, B, C or Arabic equivalents) or a sentence completion task. Prompts may optionally include location context at three levels: none, region, or region+country. Input language is either English or Modern Standard Arabic.

**Output**: For MCQ: a single character corresponding to the highest-probability option (A/B/C or Arabic letters). For closed-weight models: a JSON object containing only the answer character. For sentence completion: a likelihood score for each candidate continuation.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- MCQ evaluation yields significantly higher accuracy than sentence completion, making direct comparison with completion-based benchmarks misleading.
- Adding geographical context (region/country) does not consistently improve performance and can sometimes cause accuracy drops.
- English prompts consistently outperform Arabic prompts due to the dominance of English in instruction-tuning data, which may skew cross-lingual evaluations.

## Evidence (verbatim from paper)

> In Table[3], we observe that sentence completion is not as reliable as MCQ, despite being a more natural approach that aligns with the sentence completion framework of ArabCulture. Qwen-2.5 Instruct (32B), for example, achieves 75.2% accuracy in MCQ but drops significantly to 37.6% in sentence completion. Similar disparities are also evident in smaller models; for instance, BLOOMZ (7B) achieves 58.5% in MCQ but performs at random (31.7%) in sentence completion.

## Citation

```bibtex
@misc{sadallah2025commonsense,
  title={Commonsense Reasoning in Arab Culture},
  author={Sadallah et al. (2025)},
  year={2025},
  note={arXiv:2502.12788}
}
```

- arXiv: 2502.12788

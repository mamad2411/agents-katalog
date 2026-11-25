---
name: api-bank-eval
description: Evaluates the ability of LLMs to use external tools by testing three progressively complex capabilities: direct API slot-filling, API retrieval from a catalog, and multi-step planning combined with retrieval and calling. It measures how well models understand instructions, locate relevant functions, and generate correctly formatted calls with valid parameters. Use when the user wants to benchmark on API-Bank, or asks about evaluating this task. Reports API call correctness.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.08244
  bibtex_key: li2023apibank
  confidence: high
---

# api-bank-eval

> API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs — Minghao Li et al. (2023) (arXiv:2304.08244, 2023)

## What this evaluates

Evaluates the ability of LLMs to use external tools by testing three progressively complex capabilities: direct API slot-filling, API retrieval from a catalog, and multi-step planning combined with retrieval and calling. It measures how well models understand instructions, locate relevant functions, and generate correctly formatted calls with valid parameters.

## Datasets

- **API-Bank** — total 314; splits: test (314)

## Metrics

- `API call correctness` **(primary)** — range: percent
  - Percentage of test instances where the model correctly identifies the target API and provides all required input parameters matching the ground truth. Treated as a slot-filling task.
- `Rouge-L` — range: [0, 1]
  - Longest Common Subsequence F1 score between the model's generated response text and the reference response.

## Input / output format

**Input**: User query/instruction. In advanced settings, includes a catalog of API descriptions for retrieval. Prompts are provided in a zero-shot format.

**Output**: A structured API call (including API name and input parameters) and/or a natural language response. Exact formatting is dictated by the evaluation prompts.

## Scoring recipe

```python
def score_api_call(pred, gold):
    api_match = pred['api_name'] == gold['api_name']
    params_match = all(pred['params'].get(k) == v for k, v in gold['params'].items())
    return 1.0 if (api_match and params_match) else 0.0

def compute_accuracy(predictions, golds):
    return sum(score_api_call(p, g) for p, g in zip(predictions, golds)) / len(golds)
```

## Common pitfalls

- Zero-shot prompting makes strict adherence to the API call format difficult, causing high 'False API Call Format' error rates even when the model's intent is correct.
- Performance varies drastically across settings (Call vs Retrieve+Call vs Plan+Retrieve+Call), so reporting a single number without specifying the setting is misleading.
- Models often hallucinate APIs not present in the provided catalog, which should be counted as retrieval/call failures but are sometimes misclassified as parameter errors.

## Evidence (verbatim from paper)

> GPT-3.5 demonstrates outstanding performance in this aspect, surpassing Alpaca-7B by 35 points in API call correctness and 0.44 in the response Rouge-L score. However, the effectiveness of GPT-3.5 decreases by 21% when compared to simple API calls in the Retrieve+Call setting, and a further 17% decrease is observed in the Plan+Retrieve+Call setting.

## Citation

```bibtex
@misc{li2023apibank,
  title={API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs},
  author={Minghao Li et al. (2023)},
  year={2023},
  note={arXiv:2304.08244}
}
```

- arXiv: 2304.08244

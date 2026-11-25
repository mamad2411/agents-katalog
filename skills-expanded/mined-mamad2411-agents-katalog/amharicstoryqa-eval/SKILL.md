---
name: amharicstoryqa-eval
description: Evaluates long-sequence narrative understanding and cultural variation in Amharic using story-based question answering. Probes both multiple-choice and generative QA capabilities across different Ethiopian regional folktales. Use when the user wants to benchmark on AmharicStoryQA, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.02774
  bibtex_key: azime2026amharicstoryqa
  confidence: high
---

# amharicstoryqa-eval

> AmharicStoryQA: A Multicultural Story Question Answering Benchmark in Amharic — Azime et al. (2026) (arXiv:2602.02774, 2026)

## What this evaluates

Evaluates long-sequence narrative understanding and cultural variation in Amharic using story-based question answering. Probes both multiple-choice and generative QA capabilities across different Ethiopian regional folktales.

## Datasets

- **AmharicStoryQA** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Fraction of correctly answered questions. For multiple-choice tasks, the option appended to the prompt with the highest log-likelihood is selected as the prediction.

## Input / output format

**Input**: Question prompt with candidate options appended for multiple-choice tasks; open-ended prompts for generative tasks.

**Output**: For MCQA: the selected option string. For generative: free-form text response.

## Scoring recipe

```python
def compute_accuracy(prompts, options, gold):
    correct = 0
    for p, opts, g in zip(prompts, options, gold):
        ll = [log_likelihood(p + opt) for opt in opts]
        pred = opts[argmax(ll)]
        if pred == g: correct += 1
    return correct / len(prompts)
```

## Common pitfalls

- Option ordering bias heavily influences MCQA performance, especially in low-resource languages.
- Log-likelihood scoring for MCQA can be sensitive to prompt formatting and tokenization differences across models.

## Evidence (verbatim from paper)

> In multiple-choice each candidate option is appended to the corresponding question prompt, after which the log-likelihood is computed.Model accuracy is then reported based on the option with the highest log-likelihood score.

## Citation

```bibtex
@misc{azime2026amharicstoryqa,
  title={AmharicStoryQA: A Multicultural Story Question Answering Benchmark in Amharic},
  author={Azime et al. (2026)},
  year={2026},
  note={arXiv:2602.02774}
}
```

- arXiv: 2602.02774

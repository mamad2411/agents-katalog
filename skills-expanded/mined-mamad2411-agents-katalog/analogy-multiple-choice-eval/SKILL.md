---
name: analogy-multiple-choice-eval
description: Evaluates a language model's ability to perform analogical reasoning and select the correct word pair from multiple choices under temperature scaling. Use when the user wants to benchmark on Analogy Multiple Choice, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2302.03686
  bibtex_key: shih2023longhorizon
  confidence: high
---

# analogy-multiple-choice-eval

> Long Horizon Temperature Scaling — Shih et al. (2023) (arXiv:2302.03686, 2023)

## What this evaluates

Evaluates a language model's ability to perform analogical reasoning and select the correct word pair from multiple choices under temperature scaling.

## Datasets

- **Analogy Multiple Choice** — total 1400; splits: test (1400)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of questions where the next 8 generated tokens uniquely match the correct choice string, ignoring double matches.

## Input / output format

**Input**: Prompt containing a question, four choices, three in-context examples, and the token "Answer:".

**Output**: The model generates the next 8 tokens following "Answer:".

## Scoring recipe

```python
def score(predictions, gold):
    correct = 0
    for pred, gold_choice in zip(predictions, gold):
        if pred[:8].strip() == gold_choice.strip():
            correct += 1
    return correct / len(gold) * 100
```

## Common pitfalls

- Evaluation checks exactly the next 8 tokens, not the full generation or greedy argmax.
- Double matches are ignored to avoid penalizing models that generate the correct choice multiple times.
- The task includes a 'duplicate' variant where three choices share the first word, which significantly impacts accuracy.

## Evidence (verbatim from paper)

> To measure correctness, we check the next 8 generated tokens for a unique match with the correct choice, ignoring double matches. We also create a variant of questions where three of the choices share the first word, inspired by the example in Figure[1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Long Horizon Temperature Scaling"). The three duplicates are chosen independently from (and can include) the correct choice. In Table[1](#S6.T1 "Table 1 ‣ 6.3 Autoregressive Language Model ‣ 6 Experiments ‣ Long Horizon Temperature Scaling") we present the accuracy of GPT-2 on this analogy multiple-choice task.

## Citation

```bibtex
@misc{shih2023longhorizon,
  title={Long Horizon Temperature Scaling},
  author={Shih et al. (2023)},
  year={2023},
  note={arXiv:2302.03686}
}
```

- arXiv: 2302.03686

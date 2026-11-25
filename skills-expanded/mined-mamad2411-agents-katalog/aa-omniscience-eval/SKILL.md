---
name: aa-omniscience-eval
description: Evaluates large language models' factual recall and knowledge calibration across domain-specific questions. It measures how reliably models provide correct answers versus hallucinating or abstaining when uncertain, highlighting the gap between raw accuracy and factual reliability. Use when the user wants to benchmark on AA-Omniscience, or asks about evaluating this task. Reports Omniscience Index.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.13029
  bibtex_key: jackson2025aaomniscience
  confidence: medium
---

# aa-omniscience-eval

> AA-Omniscience: Evaluating Cross-Domain Knowledge Reliability in Large Language Models — Jackson et al. (2025) (arXiv:2511.13029, 2025)

## What this evaluates

Evaluates large language models' factual recall and knowledge calibration across domain-specific questions. It measures how reliably models provide correct answers versus hallucinating or abstaining when uncertain, highlighting the gap between raw accuracy and factual reliability.

## Datasets

- **AA-Omniscience** — total 6000; splits: test (6000)

## Metrics

- `Accuracy` — range: percent
  - Percentage of questions answered correctly by the model.
- `Hallucination Rate` — range: percent
  - Percentage of questions where the model provides a confident but incorrect answer.
- `Omniscience Index` **(primary)** — range: other
  - A bounded metric from -100 to 100 that combines accuracy, hallucination rate, and abstention behavior. It penalizes hallucinations and rewards abstention when uncertain to measure overall knowledge reliability.

## Input / output format

**Input**: Domain-specific factual questions spanning 42 economically significant topics.

**Output**: Model-generated text answers.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if is_correct(p, g))
    hallucinated = sum(1 for p, g in zip(predictions, gold) if is_confident(p) and not is_correct(p, g))
    abstained = sum(1 for p in predictions if is_abstention(p))
    total = len(predictions)
    accuracy = correct / total
    hallucination_rate = hallucinated / total
    abstention_rate = abstained / total
    # Omniscience Index conceptually combines these, penalizing hallucinations and rewarding abstention
    index = (accuracy * 100) - (hallucination_rate * 100) + (abstention_rate * 100)
    return clamp(index, -100, 100)
```

## Common pitfalls

- High accuracy does not imply factual reliability if the model frequently hallucinates.
- Overall model intelligence or parameter count does not reliably predict performance on this benchmark.
- Domain-specific performance varies significantly; overall rankings obscure specialized strengths and weaknesses.

## Evidence (verbatim from paper)

> The AA-Omniscience evaluations proves very difficult for many models, with only three frontier models at launch able to achieve an Omniscience Index score of above 0... High hallucination is the dominant factor driving these low scores. For instance, although Grok 4 and GPT-5 (high) record the highest accuracy at 39%, their hallucination rates of 64% and 81% result in substantial penalties on the Omniscience Index

## Citation

```bibtex
@misc{jackson2025aaomniscience,
  title={AA-Omniscience: Evaluating Cross-Domain Knowledge Reliability in Large Language Models},
  author={Jackson et al. (2025)},
  year={2025},
  note={arXiv:2511.13029}
}
```

- arXiv: 2511.13029

---
name: agentehr-eval
description: Evaluates autonomous clinical decision-making agents on Electronic Health Record (EHR) data. It probes multi-step reasoning, long-context dependency preservation, and robustness to distribution shifts across different hospital databases and clinical event types. Use when the user wants to benchmark on MIMIC-IV / MIMIC-III, or asks about evaluating this task. Reports average score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.13918
  bibtex_key: liao2026agentehr
  confidence: high
---

# agentehr-eval

> AgentEHR: Advancing Autonomous Clinical Decision-Making via Retrospective Summarization — Liao et al. (2026) (arXiv:2601.13918, 2026)

## What this evaluates

Evaluates autonomous clinical decision-making agents on Electronic Health Record (EHR) data. It probes multi-step reasoning, long-context dependency preservation, and robustness to distribution shifts across different hospital databases and clinical event types.

## Datasets

- **MIMIC-IV / MIMIC-III** — total ?; splits: test (-1); repo https://github.com/BlueZeros/AgentEHR

## Metrics

- `average score` **(primary)** — range: [0, 1]
  - Accuracy (or F1) averaged across six clinical event categories: Diagnoses, Labevents, Microbiology, Prescriptions, Procedures, and Transfers.

## Input / output format

**Input**: Raw, noisy Electronic Health Record (EHR) interaction history and patient data requiring multi-step clinical reasoning.

**Output**: Clinical decisions or actions corresponding to the six event categories.

## Scoring recipe

```python
def compute_metric(predictions, gold):
    categories = ['Diagnoses', 'Labevents', 'Microbiology', 'Prescriptions', 'Procedures', 'Transfers']
    scores = []
    for cat in categories:
        scores.append(accuracy_score(gold[cat], predictions[cat]))
    return sum(scores) / len(scores)
```

## Common pitfalls

- Unidirectional summary compression causes critical information loss, especially for strong backbone models.
- Evolving experience strategies show high instability and may degrade performance on weaker models.
- Distribution shifts between MIMIC-IV and MIMIC-III formats can cause severe brittleness in baseline methods.

## Evidence (verbatim from paper)

> The evolving variant of RetroSum achieves the highest average score of 0.2880.

## Citation

```bibtex
@misc{liao2026agentehr,
  title={AgentEHR: Advancing Autonomous Clinical Decision-Making via Retrospective Summarization},
  author={Liao et al. (2026)},
  year={2026},
  note={arXiv:2601.13918}
}
```

- arXiv: 2601.13918

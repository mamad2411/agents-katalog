---
name: agentrewardbench-eval
description: This benchmark evaluates the effectiveness of LLM-based judges in automatically assessing web agent trajectories. It probes the judges' ability to correctly predict task success, detect side effects, and identify repetitive actions by comparing their outputs against expert human annotations. Use when the user wants to benchmark on AgentRewardBench, or asks about evaluating this task. Reports precision.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.08942
  bibtex_key: lu2025agentrewardbench
  confidence: high
---

# agentrewardbench-eval

> AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories — Xing Han Lù et al. (2025) (arXiv:2504.08942, 2025)

## What this evaluates

This benchmark evaluates the effectiveness of LLM-based judges in automatically assessing web agent trajectories. It probes the judges' ability to correctly predict task success, detect side effects, and identify repetitive actions by comparing their outputs against expert human annotations.

## Datasets

- **AgentRewardBench** — total 1302; splits: test (-1)

## Metrics

- `precision` **(primary)** — range: [0, 1]
  - Precision is the ratio of true positives to all predicted positives (TP / (TP + FP)). It measures how many trajectories flagged as successful by the judge are actually successful according to expert annotations.
- `recall` — range: [0, 1]
  - Recall is the ratio of true positives to all actual positives (TP / (TP + FN)).
- `F1` — range: [0, 1]
  - F1 score is the harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall).

## Input / output format

**Input**: Sequence of agent thoughts and actions, plus the final browser state represented as an accessibility tree, a screenshot, or both. (NNetNav variant uses LLM-generated summaries of changes between observations.)

**Output**: Binary or categorical labels for three dimensions: success (pass/fail), side effects (present/absent), and repetition (present/absent). NNetNav outputs a 1-5 rating binarized at threshold 4.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    tp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 1)
    fp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 0)
    fn = sum(1 for p, g in zip(predictions, gold) if p == 0 and g == 1)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return {'precision': precision, 'recall': recall, 'f1': f1}
```

## Common pitfalls

- Rule-based evaluation often underestimates success by requiring exact string matches, leading to high false negative rates.
- Combining accessibility trees with screenshots can distract the judge, resulting in lower performance than using screenshots alone.

## Evidence (verbatim from paper)

> To evaluate LLM judges, we use the precision score, which is the ratio of true positives over all predicted positives (true + false positives). The metric is a good fit for rejection finetuning (RFT), where we are interested in increasing the number of true positives (actual successful trajectories) while reducing the number of false positives (failed trajectories added to the dataset due to poor LLM judgments).

## Citation

```bibtex
@misc{lu2025agentrewardbench,
  title={AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories},
  author={Xing Han Lù et al. (2025)},
  year={2025},
  note={arXiv:2504.08942}
}
```

- arXiv: 2504.08942

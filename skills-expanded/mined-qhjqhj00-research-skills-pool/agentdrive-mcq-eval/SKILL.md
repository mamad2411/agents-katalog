---
name: agentdrive-mcq-eval
description: Evaluates large language models' context-sensitive reasoning and decision-making capabilities in autonomous driving scenarios. It probes physics-based calculations, policy compliance, risk interpretation, and maneuver optimization through multiple-choice questions derived from structured driving simulations. Use when the user wants to benchmark on AgentDrive-MCQ, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.16964
  bibtex_key: ferrag2026agentdrive
  confidence: high
---

# agentdrive-mcq-eval

> AgentDrive: An Open Benchmark Dataset for Agentic AI Reasoning with LLM-Generated Scenarios in Autonomous Systems — Ferrag et al. (2026) (arXiv:2601.16964, 2026)

## What this evaluates

Evaluates large language models' context-sensitive reasoning and decision-making capabilities in autonomous driving scenarios. It probes physics-based calculations, policy compliance, risk interpretation, and maneuver optimization through multiple-choice questions derived from structured driving simulations.

## Datasets

- **AgentDrive-MCQ** — total 100000; splits: test (2000); repo https://github.com/maferrag/AgentDrive

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly answered multiple-choice questions. Calculated as (number of correct predictions / total number of questions) * 100.

## Input / output format

**Input**: A natural language description of a driving scenario (10-12 sentences) followed by a reasoning-intensive multiple-choice question with four candidate answers.

**Output**: A single selected answer choice (e.g., A, B, C, or D) corresponding to the correct option.

## Scoring recipe

```python
correct = 0
for pred, gold in zip(predictions, gold_answers):
    if pred.strip().upper() == gold.strip().upper():
        correct += 1
accuracy = (correct / len(predictions)) * 100
```

## Common pitfalls

- Models are evaluated with deterministic decoding (temperature=0.0), which may disadvantage reasoning-focused models that typically benefit from higher temperature sampling.
- The benchmark only scores the final selected answer choice, ignoring the quality or correctness of the model-generated rationale, even though rationales are part of the prompt/output structure.

## Evidence (verbatim from paper)

> We introduce AgentDrive-MCQ, a benchmark designed to probe the reasoning and decision-making capabilities of large language models (LLMs) when deployed as agentic controllers in autonomous driving. TABLE V: Accuracy (%) results of 50 examined LLM reasoning models evaluated across multiple reasoning styles using 2k samples from AgentDrive-MCQ.

## Citation

```bibtex
@misc{ferrag2026agentdrive,
  title={AgentDrive: An Open Benchmark Dataset for Agentic AI Reasoning with LLM-Generated Scenarios in Autonomous Systems},
  author={Ferrag et al. (2026)},
  year={2026},
  note={arXiv:2601.16964}
}
```

- arXiv: 2601.16964
